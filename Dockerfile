# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set environment variables to prevent .pyc files and buffering issues
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (required by some packages, e.g. for Selenium, cryptography, pydub, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    chromium-driver \
    wget \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first (if you have one) so that dependency installs can be cached
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose the port declared for the FastAPI app (9011)
EXPOSE 9011

# Use uvicorn directly to run the FastAPI app (modern and simple alternative)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9011", "--workers", "2"] 