"""AI-503: Flask REST API - model deployment + CRUD endpoints.

Run:  python -m src.api        ->  http://127.0.0.1:5000/api/health

Auth endpoints
  POST /api/auth/register        {"username", "password", "confirm", "security_question", "security_answer", ...}
  POST /api/auth/login           {"login": "user_1", "password": "..."}
  POST /api/auth/forgot          {"login": "user_1"}            -> security question
  POST /api/auth/reset           {"login", "answer", "new_password", "confirm"}
  POST /api/auth/change-password {"user_id", "current_password", "new_password", "confirm"}

AI endpoints
  GET  /api/recommend/<user_id>?n=10&model=ann&genre=Comedy
  GET  /api/similar/<movie_id>?n=10
  POST /api/predict              {"user_id": 1, "movie_id": 318, "model": "ann"}
  GET  /api/profile/<user_id>
  POST /api/chat                 {"user_id": 1, "message": "...", "history": []}
  POST /api/explain              {"user_id": 1, "model": "ann"}
  GET  /api/metrics
CRUD endpoints
  /api/movies, /api/movies/<id>       GET POST PUT DELETE
  /api/users,  /api/users/<id>        GET POST PUT DELETE
  /api/users/<id>/ratings, /api/ratings, /api/ratings/<id>
  /api/users/<id>/watchlist, /api/watchlist, /api/watchlist/<id>
"""
import sqlite3

from flask import Flask, jsonify, request

from src import auth, db, llm
from src.config import API_HOST, API_PORT
from src.dataset import load_metrics
from src.recommender import MODELS, ModelsNotTrained, get_engine

app = Flask(__name__)
app.json.sort_keys = False


def body() -> dict:
    return request.get_json(silent=True) or {}


def records(df):
    return df.astype(object).where(df.notna(), None).to_dict(orient="records")


@app.errorhandler(KeyError)
def not_found(e):
    return jsonify(error=str(e).strip("'\"")), 404


@app.errorhandler(ValueError)
def bad_request(e):
    return jsonify(error=str(e)), 400


@app.errorhandler(sqlite3.IntegrityError)
def conflict(e):
    return jsonify(error=f"Database constraint failed: {e}"), 409


@app.errorhandler(auth.AuthError)
def auth_failed(e):
    return jsonify(error=str(e)), 401 if request.path.endswith("/login") else 400


@app.errorhandler(ModelsNotTrained)
def not_trained(e):
    return jsonify(error=str(e)), 503


# ------------------------------------------------------------------ health
@app.get("/api/ping")
def ping():
    return jsonify(status="ok")


@app.get("/api/health")
def health():
    return jsonify(status="ok", counts=db.dashboard_counts(), models=list(MODELS), ollama=llm.ollama_status())


@app.get("/api/metrics")
def metrics():
    return jsonify(load_metrics())


# ------------------------------------------------------------------- auth
@app.post("/api/auth/register")
def auth_register():
    b = body()
    user = auth.register(b.get("username", ""), b.get("password", ""), b.get("confirm", b.get("password", "")),
                         b.get("security_question", ""), b.get("security_answer", ""),
                         full_name=b.get("full_name", ""), email=b.get("email", ""), age=b.get("age"),
                         gender=b.get("gender", ""))
    return jsonify(user), 201


@app.post("/api/auth/login")
def auth_login():
    b = body()
    return jsonify(auth.login(b.get("login", ""), b.get("password", "")))


@app.post("/api/auth/forgot")
def auth_forgot():
    return jsonify(security_question=auth.get_security_question(body().get("login", "")))


@app.post("/api/auth/reset")
def auth_reset():
    b = body()
    auth.reset_password_with_answer(b.get("login", ""), b.get("answer", ""), b.get("new_password", ""),
                                    b.get("confirm", b.get("new_password", "")))
    return jsonify(status="password reset")


@app.post("/api/auth/change-password")
def auth_change_password():
    b = body()
    auth.change_password(int(b["user_id"]), b.get("current_password", ""), b.get("new_password", ""),
                         b.get("confirm", b.get("new_password", "")))
    return jsonify(status="password changed")


# --------------------------------------------------------------------- AI
@app.get("/api/recommend/<int:user_id>")
def recommend(user_id):
    if not db.get_user(user_id):
        raise KeyError(f"User {user_id} not found")
    model = request.args.get("model", "ann")
    items = get_engine().recommend(user_id, int(request.args.get("n", 10)), model, request.args.get("genre", ""))
    if request.args.get("log", "1") == "1":
        db.log_recommendations(user_id, items, MODELS[model])
    return jsonify(user_id=user_id, model=MODELS[model], recommendations=items)


@app.get("/api/similar/<int:movie_id>")
def similar(movie_id):
    return jsonify(movie_id=movie_id, similar=get_engine().similar_movies(movie_id, int(request.args.get("n", 10))))


@app.post("/api/predict")
def predict():
    b = body()
    user_id, movie_id, model = int(b["user_id"]), int(b["movie_id"]), b.get("model", "ann")
    res = get_engine().predict(user_id, movie_id, model)
    db.log_prediction(user_id, movie_id, res["model"], res["probability"], res["label"])
    return jsonify(res)


@app.get("/api/profile/<int:user_id>")
def profile(user_id):
    return jsonify(get_engine().user_profile(user_id))


@app.post("/api/chat")
def chat():
    b = body()
    return jsonify(llm.chat(int(b["user_id"]), b["message"], b.get("history", []), get_engine()))


@app.post("/api/explain")
def explain():
    b = body()
    engine = get_engine()
    user_id = int(b["user_id"])
    recs = b.get("recommendations") or engine.recommend(user_id, 8, b.get("model", "ann"))
    return jsonify(explanation=llm.explain_recommendations(engine.user_profile(user_id), recs))


@app.post("/api/reload")
def reload_models():
    get_engine().refresh()
    return jsonify(status="reloaded")


# ----------------------------------------------------------------- movies
@app.get("/api/movies")
def movies_list():
    a = request.args
    return jsonify(records(db.search_movies(a.get("q", ""), a.get("genre", ""), a.get("year_from"),
                                            a.get("year_to"), int(a.get("limit", 50)))))


@app.post("/api/movies")
def movies_create():
    b = body()
    if not b.get("title"):
        raise ValueError("title is required")
    movie_id = db.create_movie(b["title"], b.get("year"), b.get("genres"), b.get("tags", ""))
    get_engine().refresh()
    return jsonify(db.get_movie(movie_id)), 201


@app.get("/api/movies/<int:movie_id>")
def movies_get(movie_id):
    movie = db.get_movie(movie_id)
    if not movie:
        raise KeyError(f"Movie {movie_id} not found")
    return jsonify(movie)


@app.put("/api/movies/<int:movie_id>")
def movies_update(movie_id):
    current = db.get_movie(movie_id)
    if not current:
        raise KeyError(f"Movie {movie_id} not found")
    b = {**current, **body()}
    db.update_movie(movie_id, b["title"], b["year"], b["genres"], b["tags"])
    get_engine().refresh()
    return jsonify(db.get_movie(movie_id))


@app.delete("/api/movies/<int:movie_id>")
def movies_delete(movie_id):
    if not db.delete_movie(movie_id):
        raise KeyError(f"Movie {movie_id} not found")
    get_engine().refresh()
    return jsonify(deleted=movie_id)


# ------------------------------------------------------------------ users
@app.get("/api/users")
def users_list():
    return jsonify(records(db.list_users()))


@app.post("/api/users")
def users_create():
    return auth_register()


@app.get("/api/users/<int:user_id>")
def users_get(user_id):
    user = db.get_user(user_id)
    if not user:
        raise KeyError(f"User {user_id} not found")
    return jsonify(user)


@app.put("/api/users/<int:user_id>")
def users_update(user_id):
    current = db.get_user(user_id)
    if not current:
        raise KeyError(f"User {user_id} not found")
    b = {**current, **body()}
    db.update_user(user_id, b["username"], b["full_name"], b["email"], b["age"], b["gender"])
    return jsonify(db.get_user(user_id))


@app.delete("/api/users/<int:user_id>")
def users_delete(user_id):
    if not db.delete_user(user_id):
        raise KeyError(f"User {user_id} not found")
    return jsonify(deleted=user_id)


# ---------------------------------------------------------------- ratings
@app.get("/api/users/<int:user_id>/ratings")
def ratings_list(user_id):
    return jsonify(records(db.get_user_ratings(user_id)))


@app.post("/api/ratings")
def ratings_upsert():
    b = body()
    db.upsert_rating(int(b["user_id"]), int(b["movie_id"]), float(b["rating"]), b.get("review", ""))
    return jsonify(status="saved"), 201


@app.delete("/api/ratings/<int:rating_id>")
def ratings_delete(rating_id):
    if not db.delete_rating(rating_id):
        raise KeyError(f"Rating {rating_id} not found")
    return jsonify(deleted=rating_id)


# -------------------------------------------------------------- watchlist
@app.get("/api/users/<int:user_id>/watchlist")
def watchlist_list(user_id):
    return jsonify(records(db.get_watchlist(user_id)))


@app.post("/api/watchlist")
def watchlist_add():
    b = body()
    db.add_to_watchlist(int(b["user_id"]), int(b["movie_id"]), b.get("status", "Plan to Watch"))
    return jsonify(status="added"), 201


@app.patch("/api/watchlist/<int:watch_id>")
def watchlist_update(watch_id):
    status = body().get("status")
    if status not in db.WATCH_STATUSES:
        raise ValueError(f"status must be one of {db.WATCH_STATUSES}")
    if not db.update_watchlist_status(watch_id, status):
        raise KeyError(f"Watchlist item {watch_id} not found")
    return jsonify(status=status)


@app.delete("/api/watchlist/<int:watch_id>")
def watchlist_delete(watch_id):
    if not db.remove_from_watchlist(watch_id):
        raise KeyError(f"Watchlist item {watch_id} not found")
    return jsonify(deleted=watch_id)


if __name__ == "__main__":
    db.init_db()
    get_engine()  # load models at startup
    app.run(host=API_HOST, port=API_PORT, debug=False)
