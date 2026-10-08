"""Feature engineering for the "Will the user like this movie?" classifiers.

Every (user, movie) pair is turned into a numeric feature vector that describes
  * the user's taste    - average rating, how generous they are, how much they rate
  * the movie's quality - average rating, popularity, release year, genres
  * the match           - how much this user likes the genres of this movie

The same function is used for training (stats from training ratings, leave-one-out
so a row never "sees" its own rating) and for live prediction (stats from the
current database), so the models work for brand-new users added through the app.
"""
import numpy as np
import pandas as pd

from src.config import GENRES, LIKE_THRESHOLD

USER_PRIOR = 5     # smoothing strength (Bayesian average) for users
MOVIE_PRIOR = 10   # smoothing strength for movies
GENRE_PRIOR = 3    # smoothing strength for user-genre affinity

GENRE_COLUMNS = ["g_" + g.replace(" ", "_").replace("(", "").replace(")", "") for g in GENRES]

FEATURE_COLUMNS = [
    "user_mean", "user_log_count", "user_like_rate",
    "movie_mean", "movie_log_count", "movie_like_rate",
    "genre_affinity", "genre_affinity_diff", "genre_like_rate",
    "year", "num_genres",
] + GENRE_COLUMNS


def movie_text(movies: pd.DataFrame) -> pd.Series:
    """Text document per movie for the TF-IDF content model: genres (weighted x3) + tags + title words."""
    title = movies["title"].fillna("").str.replace(r"\(\d{4}\)\s*$", "", regex=True)
    genres = movies["genres"].fillna("").str.replace("-", "").str.replace("|", " ", regex=False)
    tags = movies["tags"].fillna("").str.replace(",", " ")
    return (genres + " ") * 3 + tags + " " + title


def _genre_lists(movies: pd.DataFrame) -> pd.Series:
    return movies.set_index("movie_id")["genres"].fillna("(no genres listed)").str.split("|")


def build_features(stats: pd.DataFrame, movies: pd.DataFrame, pairs: pd.DataFrame, loo: bool = False) -> pd.DataFrame:
    """
    stats  : ratings used to compute user/movie statistics  (user_id, movie_id, rating)
    movies : movie catalogue                                  (movie_id, year, genres)
    pairs  : (user_id, movie_id[, rating]) rows to featurise
    loo    : leave-one-out - set True when `pairs` are rows *inside* `stats`
             (training), so each row's own rating is removed from its statistics.
    """
    pairs = pairs[["user_id", "movie_id"] + (["rating"] if loo else [])].reset_index(drop=True)
    gmean = stats["rating"].mean()
    stats = stats.assign(like=(stats["rating"] >= LIKE_THRESHOLD).astype(float))

    own_r = pairs["rating"].to_numpy() if loo else 0.0
    own_like = (pairs["rating"] >= LIKE_THRESHOLD).to_numpy().astype(float) if loo else 0.0
    own_n = 1.0 if loo else 0.0

    # ---- user statistics
    u = stats.groupby("user_id").agg(u_sum=("rating", "sum"), u_cnt=("rating", "count"), u_like=("like", "sum"))
    pu = u.reindex(pairs["user_id"]).fillna(0).to_numpy()
    u_sum, u_cnt, u_like = pu[:, 0] - own_r, pu[:, 1] - own_n, pu[:, 2] - own_like
    user_mean = (u_sum + gmean * USER_PRIOR) / (u_cnt + USER_PRIOR)
    base_like = stats["like"].mean()
    user_like_rate = (u_like + base_like * USER_PRIOR) / (u_cnt + USER_PRIOR)

    # ---- movie statistics
    m = stats.groupby("movie_id").agg(m_sum=("rating", "sum"), m_cnt=("rating", "count"), m_like=("like", "sum"))
    pm = m.reindex(pairs["movie_id"]).fillna(0).to_numpy()
    m_sum, m_cnt, m_like = pm[:, 0] - own_r, pm[:, 1] - own_n, pm[:, 2] - own_like
    movie_mean = (m_sum + gmean * MOVIE_PRIOR) / (m_cnt + MOVIE_PRIOR)
    movie_like_rate = (m_like + base_like * MOVIE_PRIOR) / (m_cnt + MOVIE_PRIOR)

    # ---- user x genre affinity
    glists = _genre_lists(movies)
    sg = stats.loc[stats["user_id"].isin(pairs["user_id"].unique()), ["user_id", "movie_id", "rating", "like"]]
    sg = sg.assign(genre=sg["movie_id"].map(glists)).explode("genre")
    ug = sg.groupby(["user_id", "genre"]).agg(g_sum=("rating", "sum"), g_cnt=("rating", "count"), g_like=("like", "sum"))

    pg = pairs[["user_id", "movie_id"]].assign(row=np.arange(len(pairs)), genre=pairs["movie_id"].map(glists))
    pg["genre"] = pg["genre"].apply(lambda g: g if isinstance(g, list) else ["(no genres listed)"])
    pg = pg.explode("genre").join(ug, on=["user_id", "genre"]).fillna({"g_sum": 0, "g_cnt": 0, "g_like": 0})
    agg = pg.groupby("row")[["g_sum", "g_cnt", "g_like"]].sum().reindex(np.arange(len(pairs))).to_numpy()
    k = pairs["movie_id"].map(glists).apply(lambda g: len(g) if isinstance(g, list) else 1).to_numpy()
    g_sum, g_cnt, g_like = agg[:, 0] - own_r * k, agg[:, 1] - own_n * k, agg[:, 2] - own_like * k
    genre_affinity = (g_sum + user_mean * GENRE_PRIOR) / (g_cnt + GENRE_PRIOR)
    genre_like_rate = (g_like + user_like_rate * GENRE_PRIOR) / (g_cnt + GENRE_PRIOR)

    # ---- movie content
    mv = movies.set_index("movie_id")
    year = pairs["movie_id"].map(mv["year"]).astype(float)
    year = year.fillna(movies["year"].median()).to_numpy()
    onehot = (
        mv["genres"].fillna("(no genres listed)").str.get_dummies("|")
        .reindex(columns=GENRES, fill_value=0)
        .reindex(pairs["movie_id"]).fillna(0).to_numpy(dtype=float)
    )

    out = pd.DataFrame({
        "user_mean": user_mean,
        "user_log_count": np.log1p(np.maximum(u_cnt, 0)),
        "user_like_rate": user_like_rate,
        "movie_mean": movie_mean,
        "movie_log_count": np.log1p(np.maximum(m_cnt, 0)),
        "movie_like_rate": movie_like_rate,
        "genre_affinity": genre_affinity,
        "genre_affinity_diff": genre_affinity - user_mean,
        "genre_like_rate": genre_like_rate,
        "year": year,
        "num_genres": k.astype(float),
    })
    out[GENRE_COLUMNS] = onehot
    return out[FEATURE_COLUMNS]
