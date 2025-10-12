# Dockerfile - general Python app (Flask/Django)
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Create a non-root user
RUN useradd -m appuser
USER appuser

ENV PYTHONUNBUFFERED=1
ENV PORT=8000

EXPOSE 8000

# Default start command (Flask: app.py -> app, Django: manage.py runserver not for prod)
# Adjust the command in Render dashboard if your entrypoint is different.
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000", "--workers", "2"]
