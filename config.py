import os

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

SAMPLE_RATE = 22050
N_MFCC = 52

HF_REPO = "srivarshini0306/body_sound_detection"

HEART_MODEL_FILE = "lstm_model.h5"
LUNG_MODEL_FILE = "lung_model.h5"

LUNG_CLASSES = ["COPD", "Bronchiolitis", "Pneumonia", "URTI", "Healthy"]
HEART_CLASSES = ["Artifact", "Murmur", "Normal"]
