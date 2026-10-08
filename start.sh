#!/usr/bin/env bash
# Starts the Flask API (background) and the Streamlit dashboard
cd "$(dirname "$0")"
[ -x .venv/bin/python ] || ./setup.sh
export TF_CPP_MIN_LOG_LEVEL=3
.venv/bin/python -m src.api &
API_PID=$!
trap 'kill $API_PID 2>/dev/null' EXIT
.venv/bin/streamlit run app.py
