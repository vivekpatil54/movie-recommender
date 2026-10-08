@echo off
REM Starts the Flask API and the Streamlit dashboard in two windows.
cd /d "%~dp0"
set TF_CPP_MIN_LOG_LEVEL=3
set TF_ENABLE_ONEDNN_OPTS=0
set PYTHONIOENCODING=utf-8

if not exist .venv\Scripts\python.exe (
    echo First run detected - running setup...
    call "%~dp0setup.bat"
)
if not exist database\movies.db (
    .venv\Scripts\python -m src.train_all
)

start "CineMind - Flask API" cmd /k .venv\Scripts\python -m src.api
start "CineMind - Streamlit" cmd /k .venv\Scripts\streamlit run app.py
echo The app will open in your browser at http://localhost:8501
timeout /t 5 >nul
start http://localhost:8501
