"""Recommendation engine: loads the saved models and serves real-time predictions.

Pipeline for personalised recommendations
  1. Candidate generation  - hybrid of content (TF-IDF) and collaborative (SVD) item similarity
                             to the movies the user rated above their own average
  2. Re-ranking            - like-probability from the chosen classifier (ANN / RF / LogReg)
  3. Explanation           - "Because you liked <movie>" from the most similar liked movie

Users with no ratings (cold start) get popular, highly-rated movies.
"""
import os
import threading

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import joblib
import numpy as np
import pandas as pd

from src import db
from src.config import (
    ANN_PATH, GENRES, LIKE_THRESHOLD, LOGREG_PATH, RF_PATH, SCALER_PATH, SVD_PATH, TFIDF_PATH,
)
from src.features import build_features, movie_text

MODELS = {
    "ann": "ANN (Keras)",
    "random_forest": "Random Forest",
    "logistic_regression": "Logistic Regression",
    "hybrid": "Hybrid similarity only",
}
CANDIDATES = 200


def _minmax(x: np.ndarray) -> np.ndarray:
    lo, hi = x.min(), x.max()
    return (x - lo) / (hi - lo) if hi > lo else np.zeros_like(x)


class ModelsNotTrained(RuntimeError):
    pass


class RecommenderEngine:
    def __init__(self):
        missing = [p.name for p in (TFIDF_PATH, SVD_PATH, LOGREG_PATH, RF_PATH) if not p.exists()]
        if missing:
            raise ModelsNotTrained(f"Missing model files {missing}. Run: python -m src.train_all")
        self.tfidf = joblib.load(TFIDF_PATH)
        svd = joblib.load(SVD_PATH)
        self._svd_index = {int(m): i for i, m in enumerate(svd["movie_ids"])}
        self._svd_factors = svd["item_factors"]
        self.classifiers = {"random_forest": joblib.load(RF_PATH), "logistic_regression": joblib.load(LOGREG_PATH)}
        self._ann = None
        self._scaler = None
        self._lock = threading.Lock()
        self.refresh()

    # ------------------------------------------------------------ data
    def refresh(self):
        """Reload the catalogue from SQLite (call after movies are added/edited/deleted)."""
        with self._lock:
            movies = db.query_df("SELECT movie_id, title, year, genres, tags FROM movies ORDER BY movie_id")
            self.movies = movies
            self.pos = {int(m): i for i, m in enumerate(movies["movie_id"])}
            self.content = self.tfidf.transform(movie_text(movies))  # rows are L2-normalised
            k = self._svd_factors.shape[1]
            self.factors = np.zeros((len(movies), k), dtype=np.float32)
            for i, m in enumerate(movies["movie_id"]):
                j = self._svd_index.get(int(m))
                if j is not None:
                    self.factors[i] = self._svd_factors[j]

    def _ratings(self) -> pd.DataFrame:
        return db.query_df("SELECT user_id, movie_id, rating FROM ratings")

    def _movie_info(self, idx: int) -> dict:
        r = self.movies.iloc[idx]
        return {
            "movie_id": int(r.movie_id),
            "title": r.title,
            "year": None if pd.isna(r.year) else int(r.year),
            "genres": r.genres,
        }

    # ------------------------------------------------------ classifiers
    def _ann_model(self):
        if self._ann is None:
            if not ANN_PATH.exists():
                raise ModelsNotTrained("ANN model not found. Run: python -m src.train_ann")
            from tensorflow import keras  # imported lazily: TensorFlow is slow to load
            self._ann = keras.models.load_model(ANN_PATH)
            self._scaler = joblib.load(SCALER_PATH)
        return self._ann

    def like_probability(self, ratings: pd.DataFrame, user_id: int, movie_ids, model: str = "ann") -> np.ndarray:
        pairs = pd.DataFrame({"user_id": user_id, "movie_id": list(movie_ids)})
        X = build_features(ratings, self.movies, pairs)
        if model == "ann":
            ann = self._ann_model()
            return ann.predict(self._scaler.transform(X), verbose=0).ravel()
        return self.classifiers[model].predict_proba(X)[:, 1]

    # ---------------------------------------------------- public API
    def popular(self, n: int = 10, genre: str = "", exclude=()) -> list:
        ratings = self._ratings()
        stats = ratings.groupby("movie_id")["rating"].agg(["mean", "count"])
        gmean, prior = ratings["rating"].mean(), 25
        stats["score"] = (stats["mean"] * stats["count"] + gmean * prior) / (stats["count"] + prior)
        stats = stats[~stats.index.isin(set(exclude))].sort_values("score", ascending=False)
        out = []
        for mid, row in stats.iterrows():
            idx = self.pos.get(int(mid))
            if idx is None:
                continue
            info = self._movie_info(idx)
            if genre and genre not in info["genres"]:
                continue
            info.update(score=round(float(row["score"]) / 5, 4),
                        reason=f"Popular pick: {row['mean']:.1f}★ from {int(row['count'])} ratings")
            out.append(info)
            if len(out) >= n:
                break
        return out

    def similar_movies(self, movie_id: int, n: int = 10) -> list:
        idx = self.pos.get(int(movie_id))
        if idx is None:
            raise KeyError(f"Movie {movie_id} not found")
        content = (self.content @ self.content[idx].T).toarray().ravel()
        has_cf = np.linalg.norm(self.factors[idx]) > 0
        score = 0.5 * content + 0.5 * (self.factors @ self.factors[idx]) if has_cf else content
        score[idx] = -np.inf
        top = np.argsort(-score)[:n]
        return [
            {**self._movie_info(i), "score": round(float(score[i]), 4),
             "reason": f"{int(round(content[i] * 100))}% content match"
                       + (", liked by similar audiences" if has_cf and self.factors[i].any() else "")}
            for i in top
        ]

    def recommend(self, user_id: int, n: int = 10, model: str = "ann", genre: str = "") -> list:
        if model not in MODELS:
            raise ValueError(f"Unknown model '{model}'. Choose from {list(MODELS)}")
        ratings = self._ratings()
        mine = ratings[ratings["user_id"] == user_id]
        mine = mine[mine["movie_id"].isin(self.pos)]
        if mine.empty:
            return self.popular(n, genre)

        # 1. Candidate generation: weighted profile of movies rated above the user's average
        rated_idx = mine["movie_id"].map(self.pos).to_numpy()
        weights = (mine["rating"] - mine["rating"].mean()).to_numpy()
        if (weights > 0).sum() == 0:
            weights = mine["rating"].to_numpy() - 2.5
        liked_mask = weights > 0
        liked_idx, w = rated_idx[liked_mask], weights[liked_mask]

        content_profile = self.content[liked_idx].T @ w
        content_score = self.content @ content_profile
        cf_score = self.factors @ (self.factors[liked_idx].T @ w)
        counts = ratings.groupby("movie_id").size().reindex(self.movies["movie_id"]).fillna(0).to_numpy()
        hybrid = 0.45 * _minmax(content_score) + 0.45 * _minmax(cf_score) + 0.10 * _minmax(np.log1p(counts))

        hybrid[rated_idx] = -np.inf
        if genre:
            hybrid[~self.movies["genres"].str.contains(genre, regex=False).to_numpy()] = -np.inf
        cand = np.argsort(-hybrid)[:CANDIDATES]
        cand = cand[np.isfinite(hybrid[cand])]
        if len(cand) == 0:
            return []

        # 2. Re-rank with the chosen classifier
        if model == "hybrid":
            final = _minmax(hybrid[cand])
            score = final
        else:
            proba = self.like_probability(ratings, user_id, self.movies["movie_id"].iloc[cand], model)
            final = 0.7 * proba + 0.3 * _minmax(hybrid[cand])
            score = proba
        order = np.argsort(-final)[:n]
        order = order[np.argsort(-score[order], kind="stable")]  # show highest match % first
        chosen = cand[order]

        # 3. Explain: the liked movie most similar (by content) to each recommendation
        sims = (self.content[chosen] @ self.content[liked_idx].T).toarray()
        out = []
        for row, (i, s) in enumerate(zip(chosen, score[order])):
            because = self.movies.iloc[liked_idx[int(np.argmax(sims[row]))]]["title"]
            out.append({**self._movie_info(i), "score": round(float(s), 4), "reason": f"Because you liked {because}"})
        return out

    def predict(self, user_id: int, movie_id: int, model: str = "ann") -> dict:
        if model not in ("ann", "random_forest", "logistic_regression"):
            raise ValueError("model must be ann, random_forest or logistic_regression")
        if int(movie_id) not in self.pos:
            raise KeyError(f"Movie {movie_id} not found")
        ratings = self._ratings()
        p = float(self.like_probability(ratings, user_id, [movie_id], model)[0])
        label = "Like" if p >= 0.5 else "Dislike"
        already = ratings[(ratings["user_id"] == user_id) & (ratings["movie_id"] == movie_id)]
        return {
            **self._movie_info(self.pos[int(movie_id)]),
            "model": MODELS[model],
            "probability": round(p, 4),
            "label": label,
            "already_rated": None if already.empty else float(already["rating"].iloc[0]),
        }

    def user_profile(self, user_id: int) -> dict:
        r = db.get_user_ratings(user_id)
        if r.empty:
            return {"user_id": user_id, "num_ratings": 0, "avg_rating": None, "top_genres": [],
                    "favourite_movies": [], "least_liked": []}
        g = r.assign(genre=r["genres"].str.split("|")).explode("genre")
        g = g[g["genre"].isin(GENRES[:-1])]
        genre_stats = g.groupby("genre")["rating"].agg(["mean", "count"])
        genre_stats["score"] = genre_stats["mean"] * np.log1p(genre_stats["count"])
        top = genre_stats.sort_values("score", ascending=False).head(5)
        best = r.sort_values(["rating", "created_at"], ascending=False).head(5)
        worst = r[r["rating"] < LIKE_THRESHOLD - 1].sort_values("rating").head(3)
        return {
            "user_id": user_id,
            "num_ratings": int(len(r)),
            "avg_rating": round(float(r["rating"].mean()), 2),
            "liked_pct": round(100 * float((r["rating"] >= LIKE_THRESHOLD).mean()), 1),
            "top_genres": [{"genre": k, "avg_rating": round(float(v["mean"]), 2), "count": int(v["count"])}
                           for k, v in top.iterrows()],
            "favourite_movies": [{"title": t, "rating": float(s)} for t, s in zip(best["title"], best["rating"])],
            "least_liked": [{"title": t, "rating": float(s)} for t, s in zip(worst["title"], worst["rating"])],
        }


_engine = None
_engine_lock = threading.Lock()


def get_engine() -> RecommenderEngine:
    """Process-wide singleton (models are loaded once)."""
    global _engine
    with _engine_lock:
        if _engine is None:
            _engine = RecommenderEngine()
        return _engine
