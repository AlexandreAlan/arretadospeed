FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app/ ./app/
COPY frontend/ ./frontend/

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8001", "--workers", "2"]
