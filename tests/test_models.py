"""Test cases for feature engineering, saved models, the recommender and the Flask API."""
import numpy as np
import pandas as pd
import pytest

from src import db
from src.config import ANN_PATH, LIKE_THRESHOLD, METRICS_PATH, RF_PATH
from src.features import FEATURE_COLUMNS, build_features

needs_models = pytest.mark.skipif(not (RF_PATH.exists() and ANN_PATH.exists()),
                                  reason="Run `python -m src.train_all` first")


# ---------------------------------------------------------------- features
def toy_data():
    movies = pd.DataFrame({"movie_id": [1, 2, 3], "title": ["A (2000)", "B (2001)", "C (2002)"],
                           "year": [2000, 2001, 2002], "genres": ["Action", "Comedy", "Action|Comedy"],
                           "tags": ["", "", ""]})
    ratings = pd.DataFrame({"user_id": [1, 1, 2, 2], "movie_id": [1, 2, 1, 3], "rating": [5.0, 2.0, 4.0, 3.0]})
    return movies, ratings


def test_feature_columns_and_shape():
    movies, ratings = toy_data()
    X = build_features(ratings, movies, ratings, loo=True)
    assert list(X.columns) == FEATURE_COLUMNS and len(X) == 4
    assert not X.isna().any().any()


def test_leave_one_out_removes_own_rating():
    """With LOO, a row's own rating is excluded from its user/movie statistics (prevents data leakage)."""
    movies, ratings = toy_data()
    loo = build_features(ratings, movies, ratings, loo=True).iloc[0]       # user 1, movie 1
    plain = build_features(ratings, movies, ratings, loo=False).iloc[0]
    assert np.isclose(loo["user_log_count"], np.log1p(1))   # user 1 has 2 ratings -> 1 without its own
    assert np.isclose(loo["movie_log_count"], np.log1p(1))  # movie 1 has 2 ratings -> 1 without its own
    assert np.isclose(plain["user_log_count"], np.log1p(2))

    # With realistic data volume, changing a row's own rating leaves its LOO features (almost) unchanged
    background = pd.DataFrame({"user_id": np.arange(100, 2100), "movie_id": 3, "rating": 3.5})
    big = pd.concat([ratings, background], ignore_index=True)
    changed = big.copy()
    changed.loc[0, "rating"] = 0.5
    a = build_features(big, movies, big.iloc[[0]], loo=True).iloc[0]
    b = build_features(changed, movies, changed.iloc[[0]], loo=True).iloc[0]
    leaky = build_features(changed, movies, changed.iloc[[0]], loo=False).iloc[0]
    for col in ("user_mean", "movie_mean", "genre_affinity"):
        assert abs(a[col] - b[col]) < 0.01, col
    assert abs(a["movie_mean"] - leaky["movie_mean"]) > 0.2  # without LOO the own rating leaks in


def test_features_for_new_user_and_new_movie():
    movies, ratings = toy_data()
    movies = pd.concat([movies, pd.DataFrame([{"movie_id": 9, "title": "New", "year": None,
                                               "genres": "Drama", "tags": ""}])])
    X = build_features(ratings, movies, pd.DataFrame({"user_id": [99], "movie_id": [9]}))
    assert not X.isna().any().any()
    assert X.iloc[0]["user_log_count"] == 0 and X.iloc[0]["movie_log_count"] == 0


# ------------------------------------------------------------------ models
@needs_models
def test_metrics_meet_minimum_quality():
    import json
    m = json.loads(METRICS_PATH.read_text())
    for model in (m["ann"], m["ml_classifiers"]["random_forest"], m["ml_classifiers"]["logistic_regression"]):
        assert model["accuracy"] > 0.65 and model["roc_auc"] > 0.75
    assert m["collaborative_filtering"]["svd_rmse"] < m["collaborative_filtering"]["baseline_global_mean_rmse"]


@needs_models
def test_recommendations(seeded_db):
    from src.recommender import RecommenderEngine
    e = RecommenderEngine()
    for model in ("ann", "random_forest", "logistic_regression", "hybrid"):
        recs = e.recommend(1, 10, model)
        assert len(recs) == 10
        rated = set(db.get_user_ratings(1)["movie_id"])
        assert not rated & {r["movie_id"] for r in recs}, "must not recommend already-rated movies"
        assert all(0 <= r["score"] <= 1 for r in recs)
    assert all("Comedy" in r["genres"] for r in e.recommend(1, 5, "ann", "Comedy"))


@needs_models
def test_cold_start_and_similar(seeded_db):
    from src import auth
    from src.recommender import RecommenderEngine
    e = RecommenderEngine()
    uid = auth.register("newbie", "Secret123", "Secret123", auth.SECURITY_QUESTIONS[0], "xyz")["user_id"]
    assert e.recommend(uid, 5)[0]["reason"].startswith("Popular")
    toy_story = db.find_movie_by_title("Toy Story (1995)")["movie_id"]
    assert "Toy Story 2 (1999)" in [m["title"] for m in e.similar_movies(toy_story, 10)]


@needs_models
def test_predict_probability(seeded_db):
    from src.recommender import RecommenderEngine
    res = RecommenderEngine().predict(1, 318, "ann")
    assert 0 <= res["probability"] <= 1
    assert res["label"] == ("Like" if res["probability"] >= 0.5 else "Dislike")
    assert LIKE_THRESHOLD == 4.0


# --------------------------------------------------------------------- API
@pytest.fixture
def api(seeded_db, monkeypatch):
    import src.recommender as rec
    from src.api import app
    monkeypatch.setattr(rec, "_engine", None)  # fresh engine on the temp database
    return app.test_client()


@needs_models
def test_api_auth_flow(api):
    r = api.post("/api/auth/register", json={"username": "api_user", "password": "Secret123",
                                             "security_question": "What is your favourite movie?",
                                             "security_answer": "Sholay"})
    assert r.status_code == 201
    assert api.post("/api/auth/login", json={"login": "api_user", "password": "Secret123"}).status_code == 200
    assert api.post("/api/auth/login", json={"login": "api_user", "password": "bad"}).status_code == 401
    assert api.post("/api/auth/forgot", json={"login": "api_user"}).get_json()["security_question"]
    r = api.post("/api/auth/reset", json={"login": "api_user", "answer": "sholay", "new_password": "NewPass456"})
    assert r.status_code == 200
    assert api.post("/api/auth/login", json={"login": "api_user", "password": "NewPass456"}).status_code == 200


@needs_models
def test_api_endpoints(api):
    assert api.get("/api/ping").status_code == 200
    assert len(api.get("/api/recommend/1?n=5").get_json()["recommendations"]) == 5
    assert api.get("/api/recommend/99999").status_code == 404
    assert api.post("/api/predict", json={"user_id": 1, "movie_id": 318}).status_code == 200
    r = api.post("/api/movies", json={"title": "Pathaan (2023)", "genres": "Action"})
    assert r.status_code == 201
    mid = r.get_json()["movie_id"]
    assert api.put(f"/api/movies/{mid}", json={"tags": "spy"}).get_json()["tags"] == "spy"
    assert api.delete(f"/api/movies/{mid}").status_code == 200
    assert api.get(f"/api/movies/{mid}").status_code == 404
    assert "password_hash" not in api.get("/api/users/1").get_json()
