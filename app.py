from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
import joblib

app = FastAPI()

# Globals
data = None
model = None

class PredictInput(BaseModel):
    Temperature: float
    Run_Time: float

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    global data
    try:
        data = pd.read_csv(file.file)
        if not {"Machine_ID", "Temperature", "Run_Time", "Downtime_Flag"}.issubset(data.columns):
            raise ValueError("Dataset must include 'Machine_ID', 'Temperature', 'Run_Time', and 'Downtime_Flag' columns.")
        return {"message": "File uploaded successfully.", "columns": list(data.columns)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"File upload failed: {str(e)}")

@app.post("/train")
async def train():
    global data, model
    if data is None:
        raise HTTPException(status_code=400, detail="No data uploaded. Please upload data first.")

    X = data[["Temperature", "Run_Time"]]
    y = data["Downtime_Flag"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    joblib.dump(model, "trained_model.pkl")

    return {"accuracy": accuracy, "f1_score": f1}

@app.post("/predict")
async def predict(input_data: PredictInput):
    global model
    if model is None:
        # Load pre-trained model if available
        try:
            model = joblib.load("trained_model.pkl")
        except Exception:
            raise HTTPException(status_code=400, detail="Model not trained or unavailable. Please train the model first.")

    features = [[input_data.Temperature, input_data.Run_Time]]
    prediction = model.predict(features)[0]
    confidence = max(model.predict_proba(features)[0])

    return {"Downtime": "Yes" if prediction == 1 else "No", "Confidence": round(confidence, 2)}

# Run this code locally using a command like `uvicorn filename:app --reload`
