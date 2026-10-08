"""Load the MovieLens dataset into the SQLite database.

Run:  python -m src.seed            (creates database/movies.db)
      python -m src.seed --reset    (deletes and recreates it)
"""
import argparse
import re
from datetime import datetime

import pandas as pd

from src import auth, db
from src.config import (
    ADMIN_PASSWORD, ADMIN_USERNAME, DATA_DIR, DB_PATH, DEMO_SECURITY_ANSWER, DEMO_SECURITY_QUESTION,
    DEMO_USER_PASSWORD,
)

YEAR_RE = re.compile(r"\((\d{4})\)\s*$")


def split_title_year(raw: str):
    """'Toy Story (1995)' -> ('Toy Story (1995)', 1995). Title is kept as-is (MovieLens style)."""
    m = YEAR_RE.search(raw.strip())
    return raw.strip(), int(m.group(1)) if m else None


def load_raw():
    movies = pd.read_csv(DATA_DIR / "movies.csv")
    ratings = pd.read_csv(DATA_DIR / "ratings.csv")
    tags = pd.read_csv(DATA_DIR / "tags.csv")
    links = pd.read_csv(DATA_DIR / "links.csv", dtype={"imdbId": str, "tmdbId": str})
    return movies, ratings, tags, links


def seed(reset: bool = False):
    if reset and DB_PATH.exists():
        DB_PATH.unlink()
    db.init_db()

    if db.dashboard_counts()["movies"] > 0:
        seed_accounts()  # make sure older databases get the login accounts too
        print("Database already seeded. Use --reset to rebuild.")
        return

    movies, ratings, tags, links = load_raw()

    # Aggregate free-text tags per movie (lower-cased, de-duplicated)
    tags["tag"] = tags["tag"].astype(str).str.lower().str.strip()
    movie_tags = tags.groupby("movieId")["tag"].apply(lambda s: ", ".join(sorted(set(s)))).rename("tags")

    movies = movies.merge(links, on="movieId", how="left").merge(movie_tags, on="movieId", how="left")
    movies["tags"] = movies["tags"].fillna("")
    movies[["title", "year"]] = movies["title"].apply(lambda t: pd.Series(split_title_year(t)))

    created = db.now()
    with db.get_conn() as conn:
        conn.executemany(
            "INSERT INTO movies (movie_id, title, year, genres, tags, imdb_id, tmdb_id, created_at) VALUES (?,?,?,?,?,?,?,?)",
            [
                (int(r.movieId), r.title, None if pd.isna(r.year) else int(r.year), r.genres, r.tags,
                 r.imdbId, None if pd.isna(r.tmdbId) else r.tmdbId, created)
                for r in movies.itertuples()
            ],
        )
        user_ids = sorted(ratings["userId"].unique())
        conn.executemany(
            "INSERT INTO users (user_id, username, full_name, email, age, gender, created_at) VALUES (?,?,?,?,?,?,?)",
            [(int(u), f"user_{u}", f"MovieLens User {u}", "", None, "", created) for u in user_ids],
        )
        conn.executemany(
            "INSERT INTO ratings (user_id, movie_id, rating, review, created_at) VALUES (?,?,?,?,?)",
            [
                (int(r.userId), int(r.movieId), float(r.rating), "",
                 datetime.fromtimestamp(int(r.timestamp)).isoformat(timespec="seconds"))
                for r in ratings.itertuples()
            ],
        )

    seed_accounts()
    print("Seeded:", db.dashboard_counts())


def seed_accounts():
    """Give MovieLens users a demo password and create the admin account."""
    # One hash shared by all demo users (hashing 610 passwords one by one would take a minute)
    pw_hash = auth.hash_secret(DEMO_USER_PASSWORD)
    ans_hash = auth.hash_secret(DEMO_SECURITY_ANSWER)
    db._execute(
        "UPDATE users SET password_hash = ?, security_question = ?, security_answer_hash = ? WHERE password_hash IS NULL",
        (pw_hash, DEMO_SECURITY_QUESTION, ans_hash),
    )
    if not auth._find_auth_row(ADMIN_USERNAME):
        auth.register(ADMIN_USERNAME, ADMIN_PASSWORD, ADMIN_PASSWORD, DEMO_SECURITY_QUESTION, DEMO_SECURITY_ANSWER,
                      full_name="System Administrator", role="admin")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="delete and rebuild the database")
    seed(parser.parse_args().reset)
