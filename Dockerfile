FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV APP_PLATFORM=WEB

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY web-requirements.txt .

RUN python -m venv .venv

RUN .venv/bin/pip install --no-cache-dir -r web-requirements.txt

COPY . .

EXPOSE 8550

CMD [".venv/bin/python", "main_web.py"]