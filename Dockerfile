# --- Build Stage for React Frontend ---
FROM node:18-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# --- Final Stage for Python Backend & Streamlit ---
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download models from Hugging Face to bake into the image
RUN python3 -c "from huggingface_hub import hf_hub_download; \
    hf_hub_download(repo_id='srivarshini0306/body_sound_detection', filename='lstm_model.h5'); \
    hf_hub_download(repo_id='srivarshini0306/body_sound_detection', filename='lung_model.h5')"

# Copy the rest of the application
COPY . .

# Copy the built frontend from the builder stage
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

# Expose ports:
# 8000: FastAPI Backend + React Frontend
# 8501: Streamlit Dashboard
EXPOSE 8000 8501

# Make the start script executable and fix line endings
RUN apt-get update && apt-get install -y dos2unix && \
    dos2unix start.sh && \
    chmod +x start.sh

# Run both processes via the start script
CMD ["./start.sh"]
