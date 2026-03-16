import os
import pickle
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# 1. Ensure the 'model' folder exists
os.makedirs('model', exist_ok=True)

# 2. Load and Prepare Data
iris = load_iris()
X, y = iris.data, iris.target

scaler = StandardScaler()
X = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Train a Lightweight Random Forest instead of a heavy Neural Network
print("Training the Random Forest model...")
model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X_train, y_train)

acc = model.score(X_test, y_test)
print(f"Training done. Final Accuracy: {acc:.2f}")

# 4. Export the Brain and the Scaler (Both as light .pkl files!)
with open("model/iris_model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("model/scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)
    
print("SUCCESS: Model and Scaler saved!")