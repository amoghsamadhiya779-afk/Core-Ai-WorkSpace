# 1. Start with the Linux Python environment
FROM python:3.10-slim

# 2. Create the working directory
WORKDIR /app

# 3. THE FIX: We tell Linux exactly what to install directly, bypassing Windows files!
RUN pip install --no-cache-dir tensorflow scikit-learn fastapi uvicorn pydantic numpy

# 4. Copy your code and the AI Brain into the container
COPY main.py .
COPY model/ ./model/

# 5. Open the port
EXPOSE 8000

# 6. THE FIX #2: Force Python to find Uvicorn directly
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]