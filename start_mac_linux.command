#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

PYTHON_CMD=""
if command -v python3 >/dev/null 2>&1; then
  PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_CMD="python"
fi

if [ -z "$PYTHON_CMD" ]; then
  echo ""
  echo "Python 3 was not found on your computer."
  echo "On macOS, you can install it via Homebrew (brew install python) or https://www.python.org/downloads/"
  echo "On Ubuntu/Debian Linux, run: sudo apt update && sudo apt install -y python3-venv python3-pip"
  echo ""
  read -r -p "Press Enter to exit..."
  exit 1
fi

if [ ! -d ".venv" ]; then
  echo "Creating a local app environment..."
  "$PYTHON_CMD" -m venv .venv
fi

# shellcheck disable=SC1091
source ".venv/bin/activate"

echo "Installing or updating required packages..."
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

if [ ! -f ".env" ] && [ -f ".env.example" ]; then
  cp ".env.example" ".env"
fi

echo "Opening your browser app..."
streamlit run app.py