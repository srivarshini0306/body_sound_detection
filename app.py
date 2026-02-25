import streamlit as st
import numpy as np
import requests
import io
import librosa
import matplotlib.pyplot as plt

from config import LUNG_CLASSES, HEART_CLASSES

API_BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="Cardio–Pulmonary AI Dashboard", layout="centered")
st.title("🫀🫁 Cardio–Pulmonary AI Dashboard")
st.markdown("---")

mode = st.sidebar.selectbox("Select Diagnosis Type", ["Heart Murmur", "Lung Disease"])
uploaded_file = st.file_uploader("Upload Audio File (.wav / .mp3)", type=["wav", "mp3"])

def plot_waveform(y, sr):
    fig, ax = plt.subplots(figsize=(10, 4))
    librosa.display.waveshow(y, sr=sr, ax=ax)
    ax.set_title("Audio Waveform")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    return fig

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')
    
    # Load for visualization
    try:
        y, sr = librosa.load(uploaded_file, sr=None)
        st.pyplot(plot_waveform(y, sr))
    except Exception as e:
        st.warning(f"Could not load waveform visualization: {e}")

    if st.button("Run Diagnosis"):
        with st.spinner("Analyzing audio via API..."):
            try:
                # Reset file pointer for requests
                uploaded_file.seek(0)
                files = {"file": (uploaded_file.name, uploaded_file.read(), uploaded_file.type)}
                
                endpoint = "/predict/heart" if mode == "Heart Murmur" else "/predict/lung"
                response = requests.post(f"{API_BASE_URL}{endpoint}", files=files)
                response.raise_for_status()
                result = response.json()

                if mode == "Heart Murmur":
                    st.success(f"Predicted Disease: {result['predicted_disease']}")
                    st.info(f"Confidence: {result['confidence']*100:.2f}%")
                    st.bar_chart(result['all_probabilities'])
                else:
                    st.success(f"Predicted Disease: {result['disease']}")
                    st.info(f"Confidence: {result['confidence']*100:.2f}%")
                    st.bar_chart(result['all_probabilities'])
                    
            except Exception as e:
                st.error(f"Error communicating with API: {e}")
                st.info("Make sure the FastAPI server is running with: uvicorn main:app --reload")

st.sidebar.markdown("""
---
### System Status
Backend: [API Link](http://localhost:8000)
""")
