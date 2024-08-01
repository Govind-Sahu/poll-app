# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables to prevent Python from writing pyc files to disk and to buffer stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the Docker container
WORKDIR /django

# Install system dependencies
RUN apt-get update \
    && apt-get install -y \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file into the working directory inside the Docker container
COPY requirements.txt /django/

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the entire Django project into the working directory inside the Docker container
COPY . /django/

# Expose the port the app runs on
EXPOSE 8000

# Run the application using Gunicorn
CMD ["gunicorn", "pollster.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
