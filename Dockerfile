# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set a working directory inside the container
WORKDIR /app

# Copy the local files to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt

# Expose a port if your bot is running a web server (optional, e.g., for webhook handling)
EXPOSE 8080

# Define the command to run your application
CMD ["uvicorn", "bot:app", "--host", "0.0.0.0", "--port", "8080"]

