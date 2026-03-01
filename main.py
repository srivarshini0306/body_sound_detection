import os
import numpy as np
import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import Dict, Any

from config import LUNG_CLASSES, HEART_CLASSES
from audio.heart_preprocessing import load_heart_audio, extract_heart_mfcc
from audio.lung_preprocessing import extract_lung_mfcc
from model.heart_model_loader import load_heart_model
from model.lung_model_loader import load_lung_model
from utils.logger import setup_logger

# Initialize Logger
logger = setup_logger("api_server")

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
try:
    logger.info("Loading models...")
    heart_model = load_heart_model()
    lung_model = load_lung_model()
    logger.info("Models loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load models: {e}")
    raise RuntimeError(f"Critical error: Could not load models. {e}")

# --- Global Exception Handler ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error at {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred. Please check the logs."},
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTP {exc.status_code} at {request.url}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# --- Helper Functions ---
async def save_temp_file(file: UploadFile) -> str:
    temp_path = f"temp_{file.filename}"
    try:
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        return temp_path
    except Exception as e:
        logger.error(f"Error saving temp file: {e}")
        raise HTTPException(status_code=500, detail="Failed to process uploaded file.")

def cleanup_temp_file(path: str):
    if os.path.exists(path):
        try:
            os.remove(path)
        except Exception as e:
            logger.error(f"Error removing temp file {path}: {e}")

# --- Routes ---
@app.post("/predict/heart")
async def predict_heart(file: UploadFile = File(...)):
    logger.info(f"Received heart prediction request: {file.filename}")
    
    if not file.filename.lower().endswith((".wav", ".mp3")):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a .wav or .mp3 file.")
    
    temp_path = await save_temp_file(file)
    try:
        y, sr = load_heart_audio(temp_path)
        X = extract_heart_mfcc(y, sr)
        preds = heart_model.predict(X)
        
        idx = int(np.argmax(preds))
        confidence = float(preds[0][idx])
        
        result = {
            "predicted_class": idx,
            "predicted_disease": HEART_CLASSES[idx],
            "confidence": confidence,
            "probabilities": preds.tolist()[0],
            "all_probabilities": {HEART_CLASSES[i]: float(preds[0][i]) for i in range(len(HEART_CLASSES))}
        }
        logger.info(f"Heart prediction successful: {HEART_CLASSES[idx]} ({confidence:.2%})")
        return result
    except Exception as e:
        logger.error(f"Heart prediction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
    finally:
        cleanup_temp_file(temp_path)

@app.post("/predict/lung")
async def predict_lung(file: UploadFile = File(...)):
    logger.info(f"Received lung prediction request: {file.filename}")
    
    if not file.filename.lower().endswith((".wav", ".mp3")):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a .wav or .mp3 file.")
    
    temp_path = await save_temp_file(file)
    try:
        X = extract_lung_mfcc(temp_path)
        preds = np.squeeze(lung_model.predict(X))
        
        cls_idx = int(np.argmax(preds))
        confidence = float(preds[cls_idx])
        
        result = {
            "disease": LUNG_CLASSES[cls_idx],
            "confidence": confidence,
            "all_probabilities": {LUNG_CLASSES[i]: float(preds[i]) for i in range(len(LUNG_CLASSES))}
        }
        logger.info(f"Lung prediction successful: {LUNG_CLASSES[cls_idx]} ({confidence:.2%})")
        return result
    except Exception as e:
        logger.error(f"Lung prediction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
    finally:
        cleanup_temp_file(temp_path)

# Serve React Frontend
frontend_path = os.path.join(os.getcwd(), "frontend", "dist")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
    logger.info(f"Frontend static files mounted from: {frontend_path}")
else:
    logger.warning("Frontend 'dist' folder not found. API running without frontend mounting.")

if __name__ == "__main__":
    logger.info("Starting uvicorn server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
