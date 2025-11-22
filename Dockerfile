# =============================================================================
# Dockerfile for User Management System (Django REST API)
# =============================================================================
# This Dockerfile creates a container for the Django application
# Compatible with Python 3.10
# =============================================================================

# Use official Python 3.10 image as base
FROM python:3.10-slim

# Set environment variables
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Set work directory inside the container
WORKDIR /app

# Install system dependencies required for MySQL client and other packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Required for mysqlclient
    default-libmysqlclient-dev \
    # Required for building Python packages
    gcc \
    pkg-config \
    # Required for healthchecks
    curl \
    # Clean up apt cache to reduce image size
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Copy the entire project
COPY . .

# Create logs directory
RUN mkdir -p /app/logs

# Create a non-root user for security
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port 8000 for the Django application
EXPOSE 8000

# Default command to run the application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "user_management.wsgi:application"]
