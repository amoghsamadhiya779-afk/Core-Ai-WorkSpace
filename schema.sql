/* ==========================================
   AI PREDICTION API - DATABASE SCHEMA (MySQL)
   ========================================== */

/* TABLE 1: USERS (The Data Scientists / Clients using your API) */
CREATE TABLE Users (
    user_id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    api_plan VARCHAR(20) NOT NULL
);

/* TABLE 2: AI_MODELS (The Brains you have deployed) */
CREATE TABLE AI_Models (
    model_id INT PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    framework VARCHAR(50) NOT NULL
);

/* TABLE 3: PREDICTION_LOGS (The 3rd Normal Form Bridge Table) */
CREATE TABLE Prediction_Logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    model_id INT,
    predicted_species VARCHAR(50) NOT NULL,
    confidence DECIMAL(5, 2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (model_id) REFERENCES AI_Models(model_id)
);

/* DUMMY DATA INJECTION */
INSERT INTO Users (user_id, name, api_plan) VALUES (1, 'Amogh', 'Pro');
INSERT INTO AI_Models (model_id, model_name, framework) VALUES (101, 'Iris Random Forest', 'Scikit-Learn');