@echo off
REM One-time setup for Windows: creates a virtual environment, installs packages,
REM builds the database and trains the models if they are missing.
cd /d "%~dp0"
title CineMind - Setup

where python >nul 2>nul
if errorlevel 1 (
    echo [X] Python was not found.
    echo     Install Python 3.12 from https://www.python.org/downloads/
    echo     and tick "Add python.exe to PATH" during installation.
    pause
    exit /b 1
)

python -c "import sys; v=sys.version_info[:2]; print('Python %%d.%%d found' %% v); sys.exit(0 if (3,10)<=v<=(3,12) else 1)"
if errorlevel 1 (
    echo [!] This project is tested with Python 3.10 - 3.12. Other versions may fail to install TensorFlow.
    echo     Press any key to try anyway, or close this window and install Python 3.12.
    pause
)

if not exist .venv (
    echo.
    echo [1/3] Creating virtual environment...
    python -m venv .venv || (echo [X] Could not create the virtual environment. & pause & exit /b 1)
)

echo.
echo [2/3] Installing packages (about 1.5 GB, takes 5-15 minutes the first time)...
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements.txt || (echo [X] Package installation failed. Check your internet connection and try again. & pause & exit /b 1)

echo.
echo [3/3] Preparing database and models...
set TF_CPP_MIN_LOG_LEVEL=3
set PYTHONIOENCODING=utf-8
if not exist models\ann_like_classifier.keras (
    .venv\Scripts\python -m src.train_all
) else (
    .venv\Scripts\python -m src.seed
)

echo.
echo ============================================================
echo  Setup complete!  Double-click start.bat to run the app.
echo ============================================================
pause
