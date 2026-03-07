from fastapi import FastAPI
from pydantic import BaseModel
import tensorflow as tf
import pickle
import numpy as np

# 1. Initialize FastAPI
app = FastAPI(title="Iris Species Predictor API")

# 2. Load the Brain and the Scaler ONCE when the server starts
# We do this globally so it doesn't reload for every single user request (which would be super slow)
model = tf.keras.models.load_model("model/iris_model.h5")
with open("model/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

# The Iris dataset class names mapping
CLASS_NAMES = ["Setosa", "Versicolor", "Virginica"]

# 3. Define the exact input we expect from the user
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# 4. Health Check Endpoint
@app.get("/")
def health_check():
    return {"status": "Active", "message": "Iris TF Model is loaded and ready!"}

# 5. The Prediction Endpoint
@app.post("/predict")
def predict_species(data: IrisInput):
    # Step A: Convert user JSON input into a 2D NumPy array
    input_data = np.array([[
        data.sepal_length, 
        data.sepal_width, 
        data.petal_length, 
        data.petal_width
    ]])
    
    # Step B: Scale the data using the exact same scaler from training
    scaled_data = scaler.transform(input_data)
    
    # Step C: Ask the Neural Network for a prediction
    prediction_probs = model.predict(scaled_data)
    
    # Step D: Find the highest probability (the network's final answer)
    predicted_class_index = np.argmax(prediction_probs[0])
    predicted_species = CLASS_NAMES[predicted_class_index]
    confidence = float(np.max(prediction_probs[0]))
    
    # Step E: Return the result to the user
    return {
        "predicted_species": predicted_species,
        "confidence": round(confidence * 100, 2), # e.g., 98.5%
        "model_engine": "TensorFlow"
    }