"""Central configuration: paths, constants and settings used across the project."""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DATA_DIR = BASE_DIR / "data" / "raw" / "ml-latest-small"
DB_PATH = BASE_DIR / "database" / "movies.db"
MODELS_DIR = BASE_DIR / "models"
REPORTS_DIR = BASE_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
METRICS_PATH = REPORTS_DIR / "metrics.json"

# Model artifact paths
TFIDF_PATH = MODELS_DIR / "tfidf_vectorizer.pkl"
SVD_PATH = MODELS_DIR / "svd_item_factors.pkl"
LOGREG_PATH = MODELS_DIR / "logistic_regression.pkl"
RF_PATH = MODELS_DIR / "random_forest.pkl"
SCALER_PATH = MODELS_DIR / "feature_scaler.pkl"
ANN_PATH = MODELS_DIR / "ann_like_classifier.keras"

# A rating >= this value means the user "liked" the movie (binary target)
LIKE_THRESHOLD = 4.0

# All genres present in MovieLens
GENRES = [
    "Action", "Adventure", "Animation", "Children", "Comedy", "Crime",
    "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "IMAX",
    "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western",
    "(no genres listed)",
]

# Flask API
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "5000"))
API_URL = os.getenv("API_URL", f"http://{API_HOST}:{API_PORT}")

# LLM Configuration (Gemini / Ollama)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini" if GEMINI_API_KEY else "ollama")

RANDOM_STATE = 42

# Demo accounts created by `python -m src.seed` (change them with environment variables).
# All 610 MovieLens users (user_1 ... user_610) share the demo password, so you can log in
# as any of them to see personalised recommendations built from real rating history.
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Admin@1234")
DEMO_USER_PASSWORD = os.getenv("DEMO_USER_PASSWORD", "Demo@1234")
DEMO_SECURITY_QUESTION = "What is your favourite movie?"
DEMO_SECURITY_ANSWER = os.getenv("DEMO_SECURITY_ANSWER", "movielens")
