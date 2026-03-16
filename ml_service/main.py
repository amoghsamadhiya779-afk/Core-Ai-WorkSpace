from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np

# 1. Initialize FastAPI
app = FastAPI(title="Iris Species Predictor API (Lightweight)")

# 2. Load the Brain and Scaler (No TensorFlow needed!)
with open("model/iris_model.pkl", "rb") as f:
    model = pickle.load(f)
with open("model/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

CLASS_NAMES = ["Setosa", "Versicolor", "Virginica"]

class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.post("/predict")
def predict_species(data: IrisInput):
    input_data = np.array([[
        data.sepal_length, data.sepal_width, data.petal_length, data.petal_width
    ]])
    
    scaled_data = scaler.transform(input_data)
    
    # Get prediction and probabilities from Random Forest
    predicted_class_index = model.predict(scaled_data)[0]
    prediction_probs = model.predict_proba(scaled_data)
    
    predicted_species = CLASS_NAMES[predicted_class_index]
    confidence = float(np.max(prediction_probs[0]))
    
    return {
        "predicted_species": predicted_species,
        "confidence": round(confidence * 100, 2),
        "model_engine": "Scikit-Learn Random Forest"
    }