from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

model = joblib.load("model_rf.pkl")

@app.get("/")
def home():
    return {"message": "API de prédiction immobilière"}

@app.post("/predict")
def predict(data: dict):
    df = pd.DataFrame([data])
    prediction = model.predict(df)
    
    return {
        "prediction": prediction[0]
    }