#!/bin/bash
set -e

if [ -x ".venv/Scripts/black.exe" ]; then
  # Windows
  BLACK=".venv/Scripts/black.exe"
elif [ -x ".venv/bin/black" ]; then
  # Linux / macOS (including ARM)
  BLACK=".venv/bin/black"
else
  echo "Error: black not found in virtual environment" >&2
  exit 1
fi

# Run black inside the venv, passing all arguments
"$BLACK" . --line-length 80 --exclude '.\.venv' "$@"
