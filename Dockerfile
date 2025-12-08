# syntax=docker/dockerfile:1.6
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install -U pip && \
    pip install -r requirements.txt

COPY . .

EXPOSE 5500

CMD ["gunicorn", "e_commerce_django.wsgi:application", "--bind", "0.0.0.0:5500"]
