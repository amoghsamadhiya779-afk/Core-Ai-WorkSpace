from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import mysql.connector

app = FastAPI(title="User Gateway Service (MySQL Enabled)")

# Pointing to the ML Container via Docker network
ML_SERVICE_URL = "http://iris_ml_api:8000/predict"

# =====================================================================
# 🗄️ THE DATABASE CONFIGURATION 
# Host is the exact name of the database container in docker-compose.yml
# =====================================================================
DB_CONFIG = {
    "host": "mysql_db",      
    "user": "root",
    "password": "password",
    "database": "ai_prediction_db"
}

class UserQuery(BaseModel):
    user_id: int          # Knowing WHO is asking
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.post("/ask-ai")
def ask_ai(query: UserQuery):
    # 1. Prepare data for the ML Brain
    payload = {
        "sepal_length": query.sepal_length,
        "sepal_width": query.sepal_width,
        "petal_length": query.petal_length,
        "petal_width": query.petal_width
    }
    
    try:
        # 2. Call the ML Microservice
        response = requests.post(ML_SERVICE_URL, json=payload)
        
        if response.status_code == 200:
            ai_data = response.json()
            species = ai_data['predicted_species']
            confidence = ai_data['confidence']
            
            # =========================================================
            # ⚡ PHASE 3: THE ACID TRANSACTION (Connecting to MySQL)
            # =========================================================
            try:
                db = mysql.connector.connect(**DB_CONFIG)
                cursor = db.cursor()
                
                # The exact SQL query to insert into your 3rd Normal Form table
                sql = """
                    INSERT INTO Prediction_Logs (user_id, model_id, predicted_species, confidence)
                    VALUES (%s, %s, %s, %s)
                """
                values = (query.user_id, 101, species, confidence)
                
                cursor.execute(sql, values)
                db.commit() # 🔒 DURABILITY GUARANTEE
                
                cursor.close()
                db.close()
                print(f"✅ Audit Log saved for User ID: {query.user_id}")
                
            except mysql.connector.Error as err:
                print(f"❌ Database Transaction Failed: {err}")
                raise HTTPException(status_code=500, detail="Database error occurred.")

            return {
                "status": "Success",
                "human_readable_answer": f"The AI predicts this is a {species} with {confidence}% confidence.",
                "database_status": "Transaction committed successfully"
            }
            
        else:
            raise HTTPException(status_code=500, detail="ML Service failed.")
            
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="ML Service is unreachable.")