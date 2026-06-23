from fastapi import FastAPI
from fastapi.responses import JSONResponse
import joblib
from datetime import datetime
from pathlib import Path

MODEL_FILE = "student_model.pkl"
MODEL_VERSION = "v1"

app = FastAPI(title="Student Score Prediction API")

model = None

@app.on_event("startup")
def load_model():
    global model

    if not Path(MODEL_FILE).exists():
        raise FileNotFoundError(
            f"{MODEL_FILE} not found. Run: python train.py"
        )

    model = joblib.load(MODEL_FILE)
    print(f"Loaded model: {MODEL_FILE}, version: {MODEL_VERSION}")

@app.get("/")
def home():
    return {
        "message": "Student Score Prediction API is running",
        "try": "/predict?hours=5"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_name": "student_score_model",
        "model_version": MODEL_VERSION
    }

@app.get("/predict")
def predict(hours: float):
    # Basic input validation
    if hours < 0:
        return JSONResponse(
            status_code=400,
            content={"error": "Hours cannot be negative"}
        )

    if hours > 12:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Input is outside the safe training range.",
                "message": "This model was trained for 1 to 8 study hours. Please provide a realistic value."
            }
        )

    prediction = float(model.predict([[hours]])[0])

    # Keep score within 0-100 range
    prediction = max(0, min(100, prediction))

    # Simple production-style log
    print(
        f"{datetime.now()} | model={MODEL_VERSION} | "
        f"hours={hours} | predicted_score={round(prediction, 2)}"
    )

    return {
        "hours": hours,
        "predicted_score": round(prediction, 2),
        "model_version": MODEL_VERSION
    }
