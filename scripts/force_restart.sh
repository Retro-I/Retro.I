#!/bin/bash

git fetch origin main
git checkout main
git reset --hard origin/main
git pull
source ".venv/bin/activate" && ".venv/bin/pip install -r requirements.txt"

sudo systemctl restart retroi

exit 0
