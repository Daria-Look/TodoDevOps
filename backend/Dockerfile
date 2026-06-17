# --- Backend Dockerfile ---

# Этап 1: Сборка зависимостей
FROM python:3.12-alpine AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Этап 2: Финальный образ
FROM python:3.12-alpine
WORKDIR /app
RUN apk add libpq 
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
