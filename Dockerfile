# Use an official lightweight Python image.
FROM python:3.9-slim

# Prevents Python from buffering stdout/stderr.
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container.
WORKDIR /app

# Install system dependencies (e.g., gcc for compiling some Python packages).
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy only the requirements file first for efficient caching.
COPY requirements.txt .

# Upgrade pip and install Python dependencies.
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of your application code.
COPY . .

# Optionally, run collectstatic if your Django app serves static files.
# RUN python manage.py collectstatic --noinput

# Expose port 8080 for Cloud Run.
EXPOSE 8080

# Run the application using Gunicorn.
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8080"]
