"""Loads ratings/movies from SQLite and builds the train/test split shared by all classifiers."""
import json

import pandas as pd
from sklearn.model_selection import train_test_split

from src import db
from src.config import LIKE_THRESHOLD, METRICS_PATH, RANDOM_STATE
from src.features import build_features


def load_frames():
    ratings = db.query_df("SELECT user_id, movie_id, rating FROM ratings")
    movies = db.query_df("SELECT movie_id, title, year, genres, tags FROM movies")
    return ratings, movies


def train_test_frames(test_size: float = 0.2):
    """Return (ratings, movies, train_df, test_df) using a fixed, stratified 80/20 split."""
    ratings, movies = load_frames()
    ratings["liked"] = (ratings["rating"] >= LIKE_THRESHOLD).astype(int)
    train_df, test_df = train_test_split(
        ratings, test_size=test_size, random_state=RANDOM_STATE, stratify=ratings["liked"]
    )
    return ratings, movies, train_df.reset_index(drop=True), test_df.reset_index(drop=True)


def classification_data():
    """Feature matrices for the like/dislike classifiers (no information leaks from test into train)."""
    ratings, movies, train_df, test_df = train_test_frames()
    X_train = build_features(train_df, movies, train_df, loo=True)
    X_test = build_features(train_df, movies, test_df, loo=False)
    return X_train, train_df["liked"].to_numpy(), X_test, test_df["liked"].to_numpy()


def save_metrics(section: str, values: dict):
    """Merge `values` into reports/metrics.json under `section`."""
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    data = json.loads(METRICS_PATH.read_text()) if METRICS_PATH.exists() else {}
    data[section] = values
    METRICS_PATH.write_text(json.dumps(data, indent=2))


def load_metrics() -> dict:
    return json.loads(METRICS_PATH.read_text()) if METRICS_PATH.exists() else {}


def ratings_matrix_summary(ratings: pd.DataFrame) -> dict:
    n_users, n_movies = ratings["user_id"].nunique(), ratings["movie_id"].nunique()
    return {
        "users": int(n_users),
        "movies_rated": int(n_movies),
        "ratings": int(len(ratings)),
        "sparsity_pct": round(100 * (1 - len(ratings) / (n_users * n_movies)), 2),
        "liked_pct": round(100 * (ratings["rating"] >= LIKE_THRESHOLD).mean(), 2),
    }
