🚀 Core AI Microservice Architecture

Lead Developer: Amogh Samadhiya

Status: Live / Production

Deployment Environment: AWS EC2 (Ubuntu) via Docker Compose

📺 Project Demonstration

Watch the end-to-end execution of the architecture from Gateway to Database.

<video width="800" controls>
<source src="./Recording 2026-03-15 103255.mp4" type="video/mp4">
<p>Your browser does not support the video tag. <a href="./Recording%202026-03-15%20103255.mp4">Click here to watch the video.</a></p>
</video>

🏗️ System Architecture

This project is a fully containerized, 3-tier microservice application designed to serve Machine Learning predictions over a REST API while maintaining ACID-compliant audit logs.

User Gateway Service (FastAPI): Exposes the public POST /ask-ai endpoint. Acts as the orchestrator, receiving user payloads, validating them, and routing them to the internal ML network.

ML Brain Service (Scikit-Learn/FastAPI): A completely isolated inference engine. It receives clean data from the Gateway, runs it through an Iris Random Forest model, and returns a prediction and confidence score.

Audit Database (MySQL 8.0): A 3rd Normal Form (3NF) relational database. Upon successful prediction, the Gateway executes a secure transaction to log the user_id, model_id, predicted_species, and confidence.

🛠️ Technology Stack

Routing & API: FastAPI, Uvicorn, Python 3.10

Machine Learning: Scikit-Learn

Database: MySQL 8.0, mysql-connector-python

DevOps & Deployment: Docker, Docker Compose, AWS EC2 (Ubuntu Linux)

🚀 How to Run Locally

Clone the repository and navigate to the root directory.

Ensure Docker Desktop is running.

Boot the architecture:

docker-compose up --build


Access the Swagger UI for testing at: http://localhost:8001/docs

☁️ How to Run in the Cloud (AWS)

SSH into the production EC2 instance.

Navigate to the project directory: cd core-ai-workspace

Boot the architecture in detached (daemon) mode:

sudo docker-compose up -d --build


The system will remain online 24/7. Access the API via the server's public IP address on port 8001.

🧪 Example API Payload

Endpoint: POST /ask-ai

{
  "user_id": 1,
  "sepal_length": 6.5,
  "sepal_width": 3.0,
  "petal_length": 5.2,
  "petal_width": 2.0
}


Successful Response:

{
  "status": "Success",
  "human_readable_answer": "The AI predicts this is a virginica with 95.0% confidence.",
  "database_status": "Transaction committed successfully"
}
