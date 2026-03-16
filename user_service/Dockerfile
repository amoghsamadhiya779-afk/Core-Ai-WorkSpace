# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements first to cache the installations
COPY requirements.txt .

# Install the dependencies (FastAPI, Uvicorn, MySQL Connector)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code (main.py) into the container
COPY . .

# Expose the port the Gateway runs on
EXPOSE 8001

# Command to boot up the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]