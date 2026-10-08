"""Test cases for database CRUD operations."""
import sqlite3

import pytest

from src import auth, db


@pytest.fixture
def user_and_movie(empty_db):
    uid = auth.register("priya", "Secret123", "Secret123", auth.SECURITY_QUESTIONS[0], "ans")["user_id"]
    mid = db.create_movie("Jawan (2023)", 2023, "Action|Thriller", "shah rukh khan")
    return uid, mid


# ------------------------------------------------------------------ movies
def test_movie_crud(empty_db):
    mid = db.create_movie("3 Idiots (2009)", 2009, "Comedy|Drama", "college")
    assert db.get_movie(mid)["title"] == "3 Idiots (2009)"
    assert len(db.search_movies("idiots")) == 1
    assert len(db.search_movies(genre="Comedy")) == 1
    assert len(db.search_movies(genre="Horror")) == 0
    db.update_movie(mid, "3 Idiots (2009)", 2009, "Comedy|Drama|Romance", "college, aamir khan")
    assert "Romance" in db.get_movie(mid)["genres"]
    assert db.delete_movie(mid) == 1
    assert db.get_movie(mid) is None


def test_movie_default_genre(empty_db):
    mid = db.create_movie("Untitled")
    assert db.get_movie(mid)["genres"] == "(no genres listed)"


def test_find_movie_by_partial_title(user_and_movie):
    assert db.find_movie_by_title("jawan")["title"] == "Jawan (2023)"
    assert db.find_movie_by_title("does not exist") is None


# ------------------------------------------------------------------- users
def test_user_update_and_list(user_and_movie):
    uid, _ = user_and_movie
    db.update_user(uid, "priya", "Priya Shah", "priya@example.com", 21, "Female")
    u = db.get_user(uid)
    assert u["full_name"] == "Priya Shah" and u["age"] == 21
    assert "password_hash" not in db.list_users().columns


def test_set_role(user_and_movie):
    uid, _ = user_and_movie
    db.set_user_role(uid, "admin")
    assert db.get_user(uid)["role"] == "admin"
    with pytest.raises(ValueError):
        db.set_user_role(uid, "superuser")


# ----------------------------------------------------------------- ratings
def test_rating_create_update_delete(user_and_movie):
    uid, mid = user_and_movie
    db.upsert_rating(uid, mid, 4.5, "Great action")
    r = db.get_user_ratings(uid)
    assert len(r) == 1 and r.iloc[0]["rating"] == 4.5
    db.upsert_rating(uid, mid, 3.0, "Changed my mind")  # same user+movie -> update, not duplicate
    r = db.get_user_ratings(uid)
    assert len(r) == 1 and r.iloc[0]["rating"] == 3.0
    db.delete_rating(int(r.iloc[0]["rating_id"]))
    assert db.get_user_ratings(uid).empty


@pytest.mark.parametrize("bad", [0, 5.5, -1])
def test_rating_out_of_range_rejected(user_and_movie, bad):
    uid, mid = user_and_movie
    with pytest.raises(sqlite3.IntegrityError):
        db.upsert_rating(uid, mid, bad)


# --------------------------------------------------------------- watchlist
def test_watchlist_crud(user_and_movie):
    uid, mid = user_and_movie
    db.add_to_watchlist(uid, mid)
    wl = db.get_watchlist(uid)
    assert wl.iloc[0]["status"] == "Plan to Watch"
    db.update_watchlist_status(int(wl.iloc[0]["watch_id"]), "Watched")
    assert db.get_watchlist(uid).iloc[0]["status"] == "Watched"
    db.add_to_watchlist(uid, mid)  # adding again must not duplicate
    assert len(db.get_watchlist(uid)) == 1
    db.remove_from_watchlist(int(wl.iloc[0]["watch_id"]))
    assert db.get_watchlist(uid).empty


# ------------------------------------------------------- logs + cascade
def test_history_and_predictions(user_and_movie):
    uid, mid = user_and_movie
    db.log_recommendations(uid, [{"movie_id": mid, "score": 0.9}], "ANN (Keras)")
    assert len(db.get_recommendation_history(uid)) == 1
    pid = db.log_prediction(uid, mid, "ANN (Keras)", 0.8, "Like")
    assert db.get_predictions(uid).iloc[0]["label"] == "Like"
    db.delete_prediction(pid)
    db.clear_recommendation_history(uid)
    assert db.get_predictions(uid).empty and db.get_recommendation_history(uid).empty


def test_delete_user_cascades(user_and_movie):
    uid, mid = user_and_movie
    db.upsert_rating(uid, mid, 4)
    db.add_to_watchlist(uid, mid)
    db.delete_user(uid)
    assert db.dashboard_counts()["ratings"] == 0
    assert db.dashboard_counts()["watchlist"] == 0


def test_delete_movie_cascades(user_and_movie):
    uid, mid = user_and_movie
    db.upsert_rating(uid, mid, 4)
    db.delete_movie(mid)
    assert db.get_user_ratings(uid).empty


def test_migration_adds_auth_columns(tmp_path, monkeypatch):
    """An old database without auth columns is upgraded by init_db()."""
    path = tmp_path / "old.db"
    con = sqlite3.connect(path)
    con.execute("CREATE TABLE users (user_id INTEGER PRIMARY KEY, username TEXT UNIQUE, full_name TEXT, "
                "email TEXT, age INTEGER, gender TEXT, created_at TEXT)")
    con.close()
    monkeypatch.setattr(db, "DB_PATH", path)
    db.init_db()
    cols = {r["name"] for r in db.query_df("PRAGMA table_info(users)").to_dict("records")}
    assert {"password_hash", "role", "failed_attempts"} <= cols
