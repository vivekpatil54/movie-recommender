# 🎬 AI Based Movie Recommendation System

TYBCA (AI & Data Analytics) Semester-V · Minor Project 2026-27 · **Group 107**
Guide: Pooja Madam · Members: Patil Vivek Raghunath (22), Sosa Divyang Govind (32)

An AI-powered movie recommendation web application with full CRUD, three machine-learning
approaches, a Keras neural network, and an open-source LLM assistant.

## Design

The dashboard is branded **CineMind** with a custom "Cinema Night" theme (`.streamlit/config.toml` + `src/theme.py`):
dark midnight background, crimson-to-violet gradients, Inter/Poppins fonts, Material icons, glass cards,
genre-coloured "posters" with animated match rings, animated stats and bars, a hero banner, and an animated
sign-in screen. Animations respect the operating system's *reduce motion* setting.

## Syllabus coverage

| Subject | What is implemented | Where |
|---|---|---|
| **AI-503** Machine Learning, Streamlit, Flask, Deployment, SQLite CRUD | TF-IDF content model, SVD collaborative filtering, Random Forest & Logistic Regression classifiers; Flask REST API; Streamlit dashboard; SQLite with 6 tables | `src/train_ml.py`, `src/api.py`, `app.py`, `src/db.py` |
| **AI-504** Open-source LLM, Prompt Engineering, AI Agents, LangChain/Ollama | MovieBot: LangChain tool-calling agent on Ollama (llama3.2) with 7 tools; prompt-engineered chains for explanations and Taste Report | `src/llm.py`, `views/moviebot.py` |
| **AI-505** ANN, Deep Learning, TensorFlow/Keras | 3-hidden-layer ANN (128-64-32, BatchNorm, Dropout, EarlyStopping) predicting Like/Dislike; loss/accuracy/AUC curves, confusion matrix, ROC | `src/train_ann.py` |

## User accounts & security

| Feature | Details |
|---|---|
| **Sign Up** | Username, name, email, age, gender, password (+ confirm), security question & answer |
| **Sign In** | With username **or** email; account locks for 5 minutes after 5 wrong passwords |
| **Forgot Password** | Answer your security question, then set a new password |
| **Change / Reset Password** | *My Account* page (needs current password); admins can set a temporary password for a user |
| **My Account** | Edit profile, change security question, delete own account |
| **Roles** | `user`: recommendations, MovieBot, ratings, watchlist, browse movies · `admin`: also add/edit/delete movies, manage users and roles, view the app as any user |
| **Storage** | Passwords and security answers stored only as salted PBKDF2-SHA256 hashes (200,000 iterations) |

### Demo accounts (created by `python -m src.seed`)

| Account | Username | Password |
|---|---|---|
| Administrator | `admin` | `Admin@1234` |
| MovieLens users (with real rating history) | `user_1` ... `user_610` | `Demo@1234` |

Security answer for all demo accounts: `movielens`. Change these via environment variables
(`ADMIN_PASSWORD`, `DEMO_USER_PASSWORD`, `DEMO_SECURITY_ANSWER`) before re-seeding.

## Testing

```bash
python -m pytest -v
```

77 automated test cases (all passing), results saved in `reports/test_results.txt`:

| File | Cases | What is tested |
|---|---|---|
| `tests/test_auth.py` | 36 | Hashing, sign-up validation, sign-in, lockout, forgot/reset/change password, remember-me tokens |
| `tests/test_crud.py` | 14 | Create/read/update/delete for movies, users, ratings, watchlist, logs; cascades; DB migration |
| `tests/test_models.py` | 9 | Feature engineering & data-leakage check, model quality thresholds, recommender, Flask API |
| `tests/test_ui.py` | 18 | Streamlit pages: sign in/out, sign up, forgot password, change password, role-based access |

Tests run on a temporary copy of the database, so the real data is never changed.

## Results (20% held-out test set, 20,168 ratings)

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---|---|---|---|---|
| Logistic Regression | 0.722 | 0.715 | 0.705 | 0.710 | 0.797 |
| Random Forest | 0.722 | 0.721 | 0.690 | 0.705 | 0.795 |
| **ANN (Keras)** | **0.722** | 0.707 | **0.724** | **0.715** | **0.801** |

Collaborative filtering (SVD, 50 factors): RMSE **0.922** vs 1.041 for the global-mean baseline.

All charts are in `reports/figures/`, all numbers in `reports/metrics.json`.

## Dataset

[MovieLens Latest Small](https://grouplens.org/datasets/movielens/latest/) (GroupLens Research):
100,836 ratings · 9,742 movies · 610 users · 3,683 tags. Ratings ≥ 4★ are labelled **Like**.

## How recommendations work

1. **Candidate generation**: the movies a user rated above their own average form a taste profile;
   candidates are scored by TF-IDF content similarity (genres + tags + title) and SVD item-factor
   similarity (what similar audiences liked), plus a small popularity term.
2. **Re-ranking**: the chosen classifier (ANN / Random Forest / Logistic Regression) predicts the
   probability that the user will like each candidate, using 31 engineered features
   (user taste, movie quality, user × genre affinity, year, genres).
3. **Explanation**: each pick shows the user's liked movie that is most similar to it, and the
   LLM can explain the whole list in plain English.

New users with no ratings get popular, highly-rated movies (cold start).

## Setup

Requires Python 3.10–3.12.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m src.train_all        # builds database/movies.db, trains all models (~2 min)
```

For the AI MovieBot, install [Ollama](https://ollama.com), then:

```bash
ollama pull llama3.2
```

## Run

Double-click **`start.bat`**, or run in two terminals:

```bash
python -m src.api              # Flask API  -> http://127.0.0.1:5000/api/health
streamlit run app.py           # Dashboard  -> http://localhost:8501
```

Open http://localhost:8501 and sign in (see demo accounts above) or create an account.
The dashboard also works without the Flask API: it falls back to running the models in-process.
Tick **Keep me signed in** to stay logged in for 7 days (a signed, tamper-proof cookie); changing your password signs out other remembered browsers.

## Project structure

```
app.py                  Streamlit entry point (navigation)
views/                  Streamlit pages (auth, home, recommendations, moviebot, report, CRUD, analytics, account)
tests/                  pytest test cases
src/config.py           Paths and settings
src/db.py               SQLite schema + CRUD functions
src/seed.py             Loads MovieLens CSVs into SQLite
src/features.py         Feature engineering shared by all classifiers
src/dataset.py          Train/test split + metrics file helpers
src/train_ml.py         AI-503 models + EDA charts
src/train_ann.py        AI-505 Keras ANN
src/train_all.py        Runs seed -> ML -> ANN
src/recommender.py      Recommendation engine (loads saved models, real-time prediction)
src/auth.py             Sign up / sign in / forgot, reset & change password, roles
src/api.py              Flask REST API
src/client.py           UI -> API client with local fallback
src/llm.py              AI-504 LangChain + Ollama agent and prompt chains
src/report.py           PDF Taste Report (ReportLab)
models/                 Saved models (.pkl, .keras)
reports/                metrics.json, ANN architecture, figures/
database/movies.db      SQLite database
data/raw/               MovieLens dataset
```

## Database tables

`users` · `movies` · `ratings` · `watchlist` · `recommendation_history` · `predictions`

## Flask API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/auth/register` | Sign up |
| POST | `/api/auth/login` | Sign in (401 on wrong password) |
| POST | `/api/auth/forgot` | Get security question |
| POST | `/api/auth/reset` | Reset password with security answer |
| POST | `/api/auth/change-password` | Change password |
| GET | `/api/health` | Status, record counts, Ollama status |
| GET | `/api/recommend/<user_id>?n=10&model=ann&genre=` | Personalised recommendations |
| GET | `/api/similar/<movie_id>?n=10` | Similar movies |
| POST | `/api/predict` `{user_id, movie_id, model}` | Like/Dislike probability |
| GET | `/api/profile/<user_id>` | Taste profile |
| POST | `/api/chat` `{user_id, message, history}` | MovieBot agent |
| POST | `/api/explain` `{user_id}` | LLM explanation of recommendations |
| GET | `/api/metrics` | Model evaluation metrics |
| GET/POST/PUT/DELETE | `/api/movies`, `/api/movies/<id>` | Movie CRUD |
| GET/POST/PUT/DELETE | `/api/users`, `/api/users/<id>` | User CRUD |
| GET/POST/DELETE | `/api/users/<id>/ratings`, `/api/ratings`, `/api/ratings/<id>` | Rating CRUD |
| GET/POST/PATCH/DELETE | `/api/users/<id>/watchlist`, `/api/watchlist`, `/api/watchlist/<id>` | Watchlist CRUD |

## Acknowledgement

F. Maxwell Harper and Joseph A. Konstan. 2015. *The MovieLens Datasets: History and Context.*
ACM Transactions on Interactive Intelligent Systems 5, 4: 19:1–19:19.
