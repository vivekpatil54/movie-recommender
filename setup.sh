#!/usr/bin/env bash
# One-time setup for macOS / Linux
set -e
cd "$(dirname "$0")"
PY=${PYTHON:-python3}
command -v "$PY" >/dev/null || { echo "Python 3 not found. Install Python 3.12 from https://www.python.org"; exit 1; }
"$PY" -c "import sys; v=sys.version_info[:2]; print('Python %d.%d found' % v); (3,10)<=v<=(3,12) or print('Warning: tested with Python 3.10-3.12')"
[ -d .venv ] || "$PY" -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
export TF_CPP_MIN_LOG_LEVEL=3
if [ -f models/ann_like_classifier.keras ]; then .venv/bin/python -m src.seed; else .venv/bin/python -m src.train_all; fi
echo "Setup complete! Run ./start.sh"
