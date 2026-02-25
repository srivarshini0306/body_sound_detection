import numpy as np
import os
from audio.heart_preprocessing import load_heart_audio, extract_heart_mfcc
from model.heart_model_loader import load_heart_model

# Load model
model = load_heart_model()

test_files = [
    r"c:\Users\sriva\Downloads\Cardio–Pulmonary-Disease-Detection-System\test_files\heart_testfiles\artifact__201106110909.wav",
    r"c:\Users\sriva\Downloads\Cardio–Pulmonary-Disease-Detection-System\test_files\heart_testfiles\murmur__193_1308078104592_B.wav"
]

for f in test_files:
    if os.path.exists(f):
        y, sr = load_heart_audio(f)
        X = extract_heart_mfcc(y, sr)
        preds = model.predict(X)
        idx = np.argmax(preds)
        print(f"File: {os.path.basename(f)} -> Index: {idx}")
    else:
        print(f"File not found: {f}")
