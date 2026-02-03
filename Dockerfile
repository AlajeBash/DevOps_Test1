# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set the home directory for rembg models
ENV U2NET_HOME=/app/models

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Pre-download the rembg model (U2NET) to save time during runtime
RUN mkdir -p /app/models && \
    python -c "from rembg import new_session; new_session('u2net')"

# Copy project
COPY . /app/

# Create media directory for uploads
RUN mkdir -p /app/superbasetest/media

# Expose port
EXPOSE 8000

# Run migrations and start Gunicorn using the recommended JSON form + exec
CMD ["sh", "-c", "python superbasetest/manage.py migrate && exec gunicorn --chdir superbasetest superbasetest.wsgi:application --bind 0.0.0.0:8000"]
