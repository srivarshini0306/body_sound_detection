import streamlit as st
import numpy as np
import requests
import io
import librosa
import librosa.display
import matplotlib.pyplot as plt
import os
import time

from config import LUNG_CLASSES, HEART_CLASSES

# Page Config for Premium Look
st.set_page_config(
    page_title="Cardio-Pulmonary AI Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Vibe Coding" Aesthetics
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    }
    .prediction-card {
        padding: 20px;
        border-radius: 15px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .status-online {
        color: #28a745;
        font-weight: bold;
    }
    .status-offline {
        color: #dc3545;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=100)
    st.title("Settings")
    mode = st.selectbox("Diagnosis Category", ["Heart Murmur", "Lung Disease"])
    st.markdown("---")
    st.subheader("System Status")
    
    # Simple Health Check
    try:
        requests.get(f"{API_BASE_URL}/docs", timeout=2)
        st.markdown('Backend: <span class="status-online">● Online</span>', unsafe_allow_html=True)
    except:
        st.markdown('Backend: <span class="status-offline">● Offline</span>', unsafe_allow_html=True)
    
    st.info("Ensure the FastAPI server is running on port 8000.")

# Main Header
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063176.png", width=80)
with col2:
    st.title("Cardio-Pulmonary Intelligent Diagnostic System")
    st.caption("AI-Powered acoustic analysis for early disease detection")

st.markdown("---")

# Layout
left_col, right_col = st.columns([1, 1])

with left_col:
    st.subheader("📤 Data Acquisition")
    uploaded_file = st.file_uploader("Upload Body Sound Recording (.wav / .mp3)", type=["wav", "mp3"])
    
    if uploaded_file:
        st.audio(uploaded_file, format='audio/wav')
        
        with st.expander("Waveform Visualization", expanded=True):
            try:
                with st.spinner("Generating visualization..."):
                    y, sr = librosa.load(uploaded_file, sr=None)
                    fig, ax = plt.subplots(figsize=(10, 3))
                    librosa.display.waveshow(y, sr=sr, ax=ax, color='#2E86C1')
                    ax.set_title("Acoustic Signal Waveform", fontsize=10)
                    ax.set_facecolor('#fdfdfd')
                    st.pyplot(fig)
            except Exception as e:
                st.error(f"Visualization Error: {e}")

with right_col:
    st.subheader("🔍 Analysis & Results")
    
    if uploaded_file:
        if st.button("🚀 Execute AI Diagnosis"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.text("Preprocessing audio signal...")
                progress_bar.progress(30)
                time.sleep(0.5)
                
                status_text.text("Sending data to AI Engine...")
                progress_bar.progress(60)
                
                # Reset file pointer
                uploaded_file.seek(0)
                files = {"file": (uploaded_file.name, uploaded_file.read(), uploaded_file.type)}
                
                endpoint = "/predict/heart" if mode == "Heart Murmur" else "/predict/lung"
                response = requests.post(f"{API_BASE_URL}{endpoint}", files=files)
                response.raise_for_status()
                result = response.json()
                
                progress_bar.progress(100)
                status_text.text("Analysis Complete.")
                time.sleep(0.3)
                progress_bar.empty()
                status_text.empty()

                # Display Results
                st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
                
                disease = result.get('predicted_disease') or result.get('disease')
                confidence = result['confidence']
                
                st.header(f"Result: {disease}")
                
                # Confidence Meter
                cols = st.columns([3, 1])
                with cols[0]:
                    st.progress(confidence)
                with cols[1]:
                    st.write(f"**{confidence*100:.1f}%**")
                
                st.markdown("---")
                st.subheader("Probability Distribution")
                st.bar_chart(result['all_probabilities'])
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                if "Normal" in disease or "Healthy" in disease:
                    st.balloons()
                    st.success("No significant abnormalities detected.")
                else:
                    st.warning(f"Detection identifies patterns associated with **{disease}**. Consult a specialist.")

            except requests.exceptions.ConnectionError:
                st.error("🚨 Connection Failed: Could not reach the AI Backend. Please ensure it is running.")
            except Exception as e:
                st.error(f"❌ Diagnostic Failure: {e}")
    else:
        st.info("Please upload an audio file to begin diagnosis.")

st.markdown("---")
st.caption("Disclaimer: This tool is for research purposes and does not replace professional medical diagnosis.")
