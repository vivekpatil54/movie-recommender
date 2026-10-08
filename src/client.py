"""Client used by the Streamlit UI for AI features.

Calls the Flask API (deployed model) when it is running; otherwise falls back to
running the same engine in-process so the UI always works during a demo.
"""
import time

import requests

from src import db, llm
from src.config import API_URL
from src.recommender import MODELS, get_engine

_status = {"checked": 0.0, "up": False}


def api_available() -> bool:
    if time.time() - _status["checked"] > 10:
        try:
            _status["up"] = requests.get(f"{API_URL}/api/ping", timeout=1.5).ok
        except requests.RequestException:
            _status["up"] = False
        _status["checked"] = time.time()
    return _status["up"]


def _get(path, **params):
    r = requests.get(f"{API_URL}{path}", params=params, timeout=120)
    r.raise_for_status()
    return r.json()


def _post(path, payload):
    r = requests.post(f"{API_URL}{path}", json=payload, timeout=300)
    r.raise_for_status()
    return r.json()


def recommend(user_id: int, n: int = 10, model: str = "ann", genre: str = "") -> list:
    if api_available():
        return _get(f"/api/recommend/{user_id}", n=n, model=model, genre=genre)["recommendations"]
    items = get_engine().recommend(user_id, n, model, genre)
    db.log_recommendations(user_id, items, MODELS[model])
    return items


def similar(movie_id: int, n: int = 10) -> list:
    if api_available():
        return _get(f"/api/similar/{movie_id}", n=n)["similar"]
    return get_engine().similar_movies(movie_id, n)


def predict(user_id: int, movie_id: int, model: str = "ann") -> dict:
    if api_available():
        return _post("/api/predict", {"user_id": user_id, "movie_id": movie_id, "model": model})
    res = get_engine().predict(user_id, movie_id, model)
    db.log_prediction(user_id, movie_id, res["model"], res["probability"], res["label"])
    return res


def profile(user_id: int) -> dict:
    if api_available():
        return _get(f"/api/profile/{user_id}")
    return get_engine().user_profile(user_id)


def chat(user_id: int, message: str, history: list) -> dict:
    if api_available():
        return _post("/api/chat", {"user_id": user_id, "message": message, "history": history})
    return llm.chat(user_id, message, history, get_engine())


def explain(user_id: int, recs: list) -> str:
    if api_available():
        return _post("/api/explain", {"user_id": user_id, "recommendations": recs})["explanation"]
    return llm.explain_recommendations(get_engine().user_profile(user_id), recs)


def catalogue_changed():
    """Tell the engine(s) to reload movies after a Movie CRUD operation."""
    if api_available():
        try:
            _post("/api/reload", {})
        except requests.RequestException:
            pass
    get_engine().refresh()
