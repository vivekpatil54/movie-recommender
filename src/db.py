"""SQLite database layer: schema + CRUD (Create, Read, Update, Delete) operations.

Tables
------
users                   registered users (with hashed password, security question, role)
movies                  movie catalogue
ratings                 user ratings (0.5 - 5.0) with optional review
watchlist               movies a user plans to watch / has watched
recommendation_history  every recommendation shown to a user
predictions             every like/dislike prediction made by a model
"""
import sqlite3
from contextlib import contextmanager
from datetime import datetime

import pandas as pd

from src.config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    username    TEXT NOT NULL UNIQUE,
    full_name   TEXT,
    email       TEXT,
    age         INTEGER,
    gender      TEXT,
    created_at  TEXT NOT NULL,
    password_hash        TEXT,
    security_question    TEXT,
    security_answer_hash TEXT,
    role                 TEXT NOT NULL DEFAULT 'user' CHECK (role IN ('user', 'admin')),
    failed_attempts      INTEGER NOT NULL DEFAULT 0,
    locked_until         TEXT,
    last_login           TEXT
);

CREATE TABLE IF NOT EXISTS movies (
    movie_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT NOT NULL,
    year        INTEGER,
    genres      TEXT NOT NULL DEFAULT '(no genres listed)',
    tags        TEXT DEFAULT '',
    imdb_id     TEXT,
    tmdb_id     TEXT,
    created_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ratings (
    rating_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    movie_id    INTEGER NOT NULL REFERENCES movies(movie_id) ON DELETE CASCADE,
    rating      REAL NOT NULL CHECK (rating BETWEEN 0.5 AND 5.0),
    review      TEXT DEFAULT '',
    created_at  TEXT NOT NULL,
    UNIQUE (user_id, movie_id)
);

CREATE TABLE IF NOT EXISTS watchlist (
    watch_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    movie_id    INTEGER NOT NULL REFERENCES movies(movie_id) ON DELETE CASCADE,
    status      TEXT NOT NULL DEFAULT 'Plan to Watch',
    added_at    TEXT NOT NULL,
    UNIQUE (user_id, movie_id)
);

CREATE TABLE IF NOT EXISTS recommendation_history (
    rec_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    movie_id    INTEGER NOT NULL REFERENCES movies(movie_id) ON DELETE CASCADE,
    model       TEXT NOT NULL,
    score       REAL,
    created_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS predictions (
    prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id       INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    movie_id      INTEGER NOT NULL REFERENCES movies(movie_id) ON DELETE CASCADE,
    model         TEXT NOT NULL,
    probability   REAL NOT NULL,
    label         TEXT NOT NULL,
    created_at    TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_ratings_user  ON ratings(user_id);
CREATE INDEX IF NOT EXISTS idx_ratings_movie ON ratings(movie_id);
"""

WATCH_STATUSES = ["Plan to Watch", "Watching", "Watched"]


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


@contextmanager
def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


# Columns added after the first version - added to old databases by init_db()
USER_MIGRATIONS = {
    "password_hash": "TEXT",
    "security_question": "TEXT",
    "security_answer_hash": "TEXT",
    "role": "TEXT NOT NULL DEFAULT 'user'",
    "failed_attempts": "INTEGER NOT NULL DEFAULT 0",
    "locked_until": "TEXT",
    "last_login": "TEXT",
}

# Public user columns - never return password or security-answer hashes to the UI/API
USER_COLUMNS = "user_id, username, full_name, email, age, gender, role, created_at, last_login"


def init_db():
    with get_conn() as conn:
        conn.executescript(SCHEMA)
        existing = {r["name"] for r in conn.execute("PRAGMA table_info(users)")}
        for col, ddl in USER_MIGRATIONS.items():
            if col not in existing:
                conn.execute(f"ALTER TABLE users ADD COLUMN {col} {ddl}")


def query_df(sql: str, params: tuple = ()) -> pd.DataFrame:
    with get_conn() as conn:
        return pd.read_sql_query(sql, conn, params=params)


def _one(sql: str, params: tuple = ()):
    with get_conn() as conn:
        row = conn.execute(sql, params).fetchone()
        return dict(row) if row else None


def _execute(sql: str, params: tuple = ()) -> int:
    """Run a write statement; returns lastrowid for INSERT, rowcount otherwise."""
    with get_conn() as conn:
        cur = conn.execute(sql, params)
        return cur.lastrowid if sql.lstrip().upper().startswith("INSERT") else cur.rowcount


# ---------------------------------------------------------------- Users CRUD
def create_user(username, full_name="", email="", age=None, gender="") -> int:
    return _execute(
        "INSERT INTO users (username, full_name, email, age, gender, created_at) VALUES (?,?,?,?,?,?)",
        (username.strip(), full_name, email, age, gender, now()),
    )


def get_user(user_id: int):
    return _one(f"SELECT {USER_COLUMNS} FROM users WHERE user_id = ?", (user_id,))


def list_users() -> pd.DataFrame:
    cols = ", ".join("u." + c.strip() for c in USER_COLUMNS.split(","))
    return query_df(
        f"""SELECT {cols}, COUNT(r.rating_id) AS num_ratings
           FROM users u LEFT JOIN ratings r ON r.user_id = u.user_id
           GROUP BY u.user_id ORDER BY u.user_id"""
    )


def update_user(user_id, username, full_name, email, age, gender) -> int:
    return _execute(
        "UPDATE users SET username=?, full_name=?, email=?, age=?, gender=? WHERE user_id=?",
        (username.strip(), full_name, email, age, gender, user_id),
    )


def set_user_role(user_id: int, role: str) -> int:
    if role not in ("user", "admin"):
        raise ValueError("role must be 'user' or 'admin'")
    return _execute("UPDATE users SET role = ? WHERE user_id = ?", (role, user_id))


def delete_user(user_id: int) -> int:
    return _execute("DELETE FROM users WHERE user_id = ?", (user_id,))


# --------------------------------------------------------------- Movies CRUD
def create_movie(title, year=None, genres="(no genres listed)", tags="", imdb_id=None, tmdb_id=None) -> int:
    return _execute(
        "INSERT INTO movies (title, year, genres, tags, imdb_id, tmdb_id, created_at) VALUES (?,?,?,?,?,?,?)",
        (title.strip(), year, genres or "(no genres listed)", tags, imdb_id, tmdb_id, now()),
    )


def get_movie(movie_id: int):
    return _one(
        """SELECT m.*, ROUND(AVG(r.rating), 2) AS avg_rating, COUNT(r.rating_id) AS num_ratings
           FROM movies m LEFT JOIN ratings r ON r.movie_id = m.movie_id
           WHERE m.movie_id = ? GROUP BY m.movie_id""",
        (movie_id,),
    )


def search_movies(text: str = "", genre: str = "", year_from=None, year_to=None, limit: int = 50) -> pd.DataFrame:
    sql = """SELECT m.movie_id, m.title, m.year, m.genres,
                    ROUND(AVG(r.rating), 2) AS avg_rating, COUNT(r.rating_id) AS num_ratings
             FROM movies m LEFT JOIN ratings r ON r.movie_id = m.movie_id WHERE 1=1"""
    params = []
    if text:
        sql += " AND (m.title LIKE ? OR m.tags LIKE ?)"
        params += [f"%{text}%", f"%{text}%"]
    if genre:
        sql += " AND m.genres LIKE ?"
        params.append(f"%{genre}%")
    if year_from:
        sql += " AND m.year >= ?"
        params.append(int(year_from))
    if year_to:
        sql += " AND m.year <= ?"
        params.append(int(year_to))
    sql += " GROUP BY m.movie_id ORDER BY num_ratings DESC, m.title LIMIT ?"
    params.append(int(limit))
    return query_df(sql, tuple(params))


def list_movies() -> pd.DataFrame:
    return query_df("SELECT * FROM movies ORDER BY movie_id")


def find_movie_by_title(title: str):
    """Best match for a (partial) title: exact first, then most-rated LIKE match."""
    row = _one("SELECT * FROM movies WHERE lower(title) = lower(?)", (title.strip(),))
    if row:
        return row
    return _one(
        """SELECT m.* FROM movies m LEFT JOIN ratings r ON r.movie_id = m.movie_id
           WHERE m.title LIKE ? GROUP BY m.movie_id ORDER BY COUNT(r.rating_id) DESC LIMIT 1""",
        (f"%{title.strip()}%",),
    )


def update_movie(movie_id, title, year, genres, tags) -> int:
    return _execute(
        "UPDATE movies SET title=?, year=?, genres=?, tags=? WHERE movie_id=?",
        (title.strip(), year, genres or "(no genres listed)", tags, movie_id),
    )


def delete_movie(movie_id: int) -> int:
    return _execute("DELETE FROM movies WHERE movie_id = ?", (movie_id,))


# -------------------------------------------------------------- Ratings CRUD
def upsert_rating(user_id: int, movie_id: int, rating: float, review: str = "") -> int:
    """Create a rating, or update it if the user already rated the movie."""
    return _execute(
        """INSERT INTO ratings (user_id, movie_id, rating, review, created_at) VALUES (?,?,?,?,?)
           ON CONFLICT(user_id, movie_id) DO UPDATE SET rating=excluded.rating,
               review=excluded.review, created_at=excluded.created_at""",
        (user_id, movie_id, float(rating), review, now()),
    )


def get_user_ratings(user_id: int) -> pd.DataFrame:
    return query_df(
        """SELECT r.rating_id, r.movie_id, m.title, m.year, m.genres, r.rating, r.review, r.created_at
           FROM ratings r JOIN movies m ON m.movie_id = r.movie_id
           WHERE r.user_id = ? ORDER BY r.created_at DESC""",
        (user_id,),
    )


def delete_rating(rating_id: int) -> int:
    return _execute("DELETE FROM ratings WHERE rating_id = ?", (rating_id,))


def all_ratings() -> pd.DataFrame:
    return query_df("SELECT user_id, movie_id, rating, created_at FROM ratings")


# ------------------------------------------------------------ Watchlist CRUD
def add_to_watchlist(user_id: int, movie_id: int, status: str = "Plan to Watch") -> int:
    return _execute(
        """INSERT INTO watchlist (user_id, movie_id, status, added_at) VALUES (?,?,?,?)
           ON CONFLICT(user_id, movie_id) DO UPDATE SET status=excluded.status""",
        (user_id, movie_id, status, now()),
    )


def get_watchlist(user_id: int) -> pd.DataFrame:
    return query_df(
        """SELECT w.watch_id, w.movie_id, m.title, m.year, m.genres, w.status, w.added_at
           FROM watchlist w JOIN movies m ON m.movie_id = w.movie_id
           WHERE w.user_id = ? ORDER BY w.added_at DESC""",
        (user_id,),
    )


def update_watchlist_status(watch_id: int, status: str) -> int:
    return _execute("UPDATE watchlist SET status = ? WHERE watch_id = ?", (status, watch_id))


def remove_from_watchlist(watch_id: int) -> int:
    return _execute("DELETE FROM watchlist WHERE watch_id = ?", (watch_id,))


# ------------------------------------------------- History / prediction logs
def log_recommendations(user_id: int, items: list, model: str):
    with get_conn() as conn:
        conn.executemany(
            "INSERT INTO recommendation_history (user_id, movie_id, model, score, created_at) VALUES (?,?,?,?,?)",
            [(user_id, it["movie_id"], model, it.get("score"), now()) for it in items],
        )


def get_recommendation_history(user_id: int, limit: int = 100) -> pd.DataFrame:
    return query_df(
        """SELECT h.rec_id, h.movie_id, m.title, h.model, ROUND(h.score, 3) AS score, h.created_at
           FROM recommendation_history h JOIN movies m ON m.movie_id = h.movie_id
           WHERE h.user_id = ? ORDER BY h.rec_id DESC LIMIT ?""",
        (user_id, limit),
    )


def clear_recommendation_history(user_id: int) -> int:
    return _execute("DELETE FROM recommendation_history WHERE user_id = ?", (user_id,))


def log_prediction(user_id, movie_id, model, probability, label) -> int:
    return _execute(
        "INSERT INTO predictions (user_id, movie_id, model, probability, label, created_at) VALUES (?,?,?,?,?,?)",
        (user_id, movie_id, model, float(probability), label, now()),
    )


def get_predictions(user_id: int, limit: int = 100) -> pd.DataFrame:
    return query_df(
        """SELECT p.prediction_id, m.title, p.model, ROUND(p.probability, 3) AS probability, p.label, p.created_at
           FROM predictions p JOIN movies m ON m.movie_id = p.movie_id
           WHERE p.user_id = ? ORDER BY p.prediction_id DESC LIMIT ?""",
        (user_id, limit),
    )


def delete_prediction(prediction_id: int) -> int:
    return _execute("DELETE FROM predictions WHERE prediction_id = ?", (prediction_id,))


# ------------------------------------------------------------------- Stats
def dashboard_counts() -> dict:
    with get_conn() as conn:
        return {
            t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
            for t in ["users", "movies", "ratings", "watchlist", "recommendation_history", "predictions"]
        }
