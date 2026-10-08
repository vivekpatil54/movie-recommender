"""Tests for LLM integration (Gemini / Ollama / Fallbacks)."""
from unittest.mock import MagicMock, patch

from src import llm
from src.recommender import get_engine


def test_llm_status():
    status = llm.ollama_status()
    assert isinstance(status, dict)
    assert "model" in status
    assert "model_available" in status
    assert "running" in status


def test_fallback_explanation():
    profile = {
        "top_genres": [{"genre": "Action"}, {"genre": "Sci-Fi"}],
        "favourite_movies": [{"title": "The Matrix", "rating": 5.0}],
    }
    recs = [
        {"title": "Inception", "reason": "Because you liked The Matrix"},
        {"title": "Interstellar", "reason": "High sci-fi affinity"},
    ]
    text = llm.fallback_explanation(profile, recs)
    assert "Inception" in text
    assert "The Matrix" in text


def test_fallback_report():
    profile = {
        "num_ratings": 15,
        "avg_rating": 4.2,
        "top_genres": [{"genre": "Comedy"}],
        "favourite_movies": [{"title": "Superbad", "rating": 4.5}],
    }
    recs = [{"title": "Step Brothers", "reason": "Comedy match"}]
    text = llm.fallback_report(profile, recs)
    assert "Taste Summary:" in text
    assert "Viewing Personality:" in text
    assert "Why These Recommendations:" in text
    assert "Try Something New:" in text


def test_explain_recommendations_with_engine():
    engine = get_engine()
    profile = engine.user_profile(1)
    recs = engine.recommend(1, n=3, model="ann")
    explanation = llm.explain_recommendations(profile, recs)
    assert isinstance(explanation, str)
    assert len(explanation) > 20


def test_taste_report_with_engine():
    engine = get_engine()
    profile = engine.user_profile(1)
    recs = engine.recommend(1, n=3, model="ann")
    report = llm.taste_report("test_user", profile, recs)
    assert isinstance(report, str)
    assert len(report) > 50


def test_moviebot_chat_offline_hint(monkeypatch):
    monkeypatch.setattr(llm, "setup_hint", lambda: "Mocked offline error")
    engine = get_engine()
    res = llm.chat(1, "Hello", [], engine)
    assert "Mocked offline error" in res["reply"]
