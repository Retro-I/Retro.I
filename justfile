set shell := ["powershell", "-NoProfile", "-Command"]

VENV := ".venv"

install:
    & "{{VENV}}\Scripts\pip.exe" install -r test-requirements.txt

black:
    scripts/black.sh

flake:
    & "{{VENV}}\Scripts\flake8.exe" .

isort:
    & "{{VENV}}\Scripts\isort.exe" .

lint:
    just black
    just flake
    just isort

test:
    & "{{VENV}}\Scripts\python.exe" -m unittest
