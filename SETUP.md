# 🎬 CineMind: Setup Guide

AI Based Movie Recommendation System · TYBCA Minor Project 2026-27 · Group 107

---

## What you need

| Requirement | Notes |
|---|---|
| **Windows 10/11** (or macOS / Linux) | |
| **Python 3.12** (3.10 – 3.12 work) | Download: https://www.python.org/downloads/ |
| **Internet** | Only for the first setup (downloads about 1.5 GB of packages) |
| **About 3 GB free disk space** | |
| Ollama *(optional)* | Only needed for the AI chatbot (MovieBot). Everything else works without it. |

> ⚠️ When installing Python on Windows, tick **"Add python.exe to PATH"** on the first screen.

---

## Setup (one time only)

1. **Unzip** `movie-recommender.zip` to a simple folder, for example `C:\Projects\movie-recommender`
   (avoid very long paths and folders inside OneDrive).
2. Open the folder and **double-click `setup.bat`**.
3. Wait until it says **"Setup complete!"** (5–15 minutes the first time).

That's it.

## Run the app

1. **Double-click `start.bat`**.
2. Two black windows open (Flask API + Streamlit). **Keep them open** while using the app.
3. The browser opens **http://localhost:8501** automatically (open it yourself if it doesn't).
4. To stop the app, close the two black windows.

### macOS / Linux
```bash
chmod +x setup.sh start.sh
./setup.sh      # one time
./start.sh      # every time
```

---

## Log in

| Account | Username | Password |
|---|---|---|
| Admin (can manage movies & users) | `admin` | `Admin@1234` |
| Demo user with 232 real ratings | `user_1` | `Demo@1234` |
| Any MovieLens user | `user_2` … `user_610` | `Demo@1234` |

Security answer for demo accounts (used by Forgot Password): `movielens`

You can also click **Create an account** to sign up as a new user.

---

## Turn on the AI chatbot (optional)

1. Install Ollama from https://ollama.com and open it.
2. Open Command Prompt and run:
   ```bash
   ollama pull llama3.2
   ```
   (downloads about 2 GB, one time)
3. Restart the app with `start.bat`. The sidebar will show **LLM: Online**.

---

## Things to try

1. Log in as `user_1`, then go to **Recommendations** and click **Recommend**.
2. **Will I Like It?** tab: pick *Titanic* and see the predictions from all 3 models.
3. **Ratings & Watchlist**: rate a few movies, then get recommendations again.
4. **Taste Report**: generate and download your PDF report.
5. **Model Performance**: accuracy, ROC-AUC, confusion matrices and the ANN training curves.
6. Log in as `admin`: **Manage Users** and add/edit/delete movies on the **Movies** page.

---

## Useful commands (optional)

Run these from the project folder in Command Prompt:

```bash
.venv\Scripts\python -m pytest              # run all 77 automated tests
.venv\Scripts\python -m src.train_all       # retrain all models (~2 minutes)
.venv\Scripts\python -m src.seed --reset    # reset the database to the original data
```

---

## Problems?

| Problem | Fix |
|---|---|
| `Python was not found` | Install Python 3.12 and tick **Add python.exe to PATH**, then run `setup.bat` again |
| Package install fails / TensorFlow error | Use Python **3.12** (not 3.13 / 3.14). Delete the `.venv` folder and run `setup.bat` again |
| `Port 8501 is already in use` | Close old app windows, or restart the computer |
| Browser shows "connection refused" | Wait 10–20 seconds after `start.bat` and refresh |
| MovieBot says "offline" | Install Ollama and run `ollama pull llama3.2` (see above) |
| Forgot your password | Use **Forgot password?** on the sign-in page, or log in as `admin` and reset it |

More details are in `README.md`.
