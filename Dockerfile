# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# rembg looks here for model files
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
# Ensure onnxruntime is present for performance
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install onnxruntime

# Pre-download the rembg model (U2NET)
# This creates the /app/models/.u2net directory and downloads the model during build
RUN mkdir -p /app/models && \
    python -c "from rembg import new_session; new_session('u2net')"

# Copy project
COPY . /app/

# Create media directory for uploads
RUN mkdir -p /app/superbasetest/media

# Expose port
EXPOSE 8000

# Run migrations and start Gunicorn
CMD ["sh", "-c", "python superbasetest/manage.py migrate && exec gunicorn --chdir superbasetest superbasetest.wsgi:application --bind 0.0.0.0:8000 --timeout 120"]
