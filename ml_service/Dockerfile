FROM python:3.10-slim

WORKDIR /app

# Look at this line: No TensorFlow! This will install instantly and use almost no memory.
RUN pip install --no-cache-dir scikit-learn fastapi uvicorn pydantic numpy

COPY main.py .
COPY model/ ./model/

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]