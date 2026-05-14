FROM python:3.11-slim-bookworm

WORKDIR /app

RUN echo 'Acquire::ForceIPv4 "true";' > /etc/apt/apt.conf.d/99force-ipv4

RUN apt-get update && apt-get install -y --no-install-recommends \
    libasound2 \
    alsa-utils \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# IMPORTANT
RUN pip install --upgrade pip
RUN pip install "setuptools<58" wheel

# IMPORTANT
RUN pip install --no-build-isolation playsound==1.3.0

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["xvfb-run", "-a", "behave"]