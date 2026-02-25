import os
import io
import numpy as np
import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

from config import LUNG_CLASSES, HEART_CLASSES
from audio.heart_preprocessing import load_heart_audio, extract_heart_mfcc
from audio.lung_preprocessing import extract_lung_mfcc
from model.heart_model_loader import load_heart_model
from model.lung_model_loader import load_lung_model

app = FastAPI(title="Cardio-Pulmonary AI API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models at startup
heart_model = load_heart_model()
lung_model = load_lung_model()

@app.get("/")
async def root():
    return {"message": "Cardio-Pulmonary AI API is running"}

@app.post("/predict/heart")
async def predict_heart(file: UploadFile = File(...)):
    if not file.filename.endswith((".wav", ".mp3")):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a .wav or .mp3 file.")
    
    temp_path = f"temp_{file.filename}"
    try:
        # Save to temp file to avoid Errno 22 with BytesIO on some Windows setups
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        y, sr = load_heart_audio(temp_path)
        X = extract_heart_mfcc(y, sr)
        preds = heart_model.predict(X)
        
        from config import HEART_CLASSES
        idx = int(np.argmax(preds))
        result = {
            "predicted_class": idx,
            "predicted_disease": HEART_CLASSES[idx],
            "confidence": float(preds[0][idx]),
            "probabilities": preds.tolist()[0],
            "all_probabilities": {HEART_CLASSES[i]: float(preds[0][i]) for i in range(len(HEART_CLASSES))}
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.post("/predict/lung")
async def predict_lung(file: UploadFile = File(...)):
    if not file.filename.endswith((".wav", ".mp3")):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a .wav or .mp3 file.")
    
    temp_path = f"temp_{file.filename}"
    try:
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
            
        X = extract_lung_mfcc(temp_path)
        preds = np.squeeze(lung_model.predict(X))
        
        cls_idx = int(np.argmax(preds))
        result = {
            "disease": LUNG_CLASSES[cls_idx],
            "confidence": float(preds[cls_idx]),
            "all_probabilities": {LUNG_CLASSES[i]: float(preds[i]) for i in range(len(LUNG_CLASSES))}
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
