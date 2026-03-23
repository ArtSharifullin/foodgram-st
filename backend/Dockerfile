FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY foodgram/ /app/
COPY data/ /app/data/

EXPOSE 8000

CMD ["gunicorn", "--chdir", "/app", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120", "foodgram.wsgi:application"]
