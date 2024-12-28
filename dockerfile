# Base Image
FROM python:3.11-slim

# Set Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a non-root user
RUN useradd -m django

# Set Working Directory
WORKDIR /app

# Install System Dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python Dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy Project Files
COPY . .

# Switch to the django user
USER django

# Expose Port
EXPOSE 8000

# Production-ready Command
CMD ["gunicorn", "your_project.wsgi:application", "--bind", "0.0.0.0:8000"]
