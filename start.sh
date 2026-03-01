#!/bin/bash

# Start the FastAPI backend in the background
# It serves the API at port 8000 and the React frontend (if built)
echo "Starting FastAPI backend..."
python main.py &

# Start the Streamlit dashboard
echo "Starting Streamlit dashboard..."
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

# Wait for background processes to finish (optional, keep container alive)
wait
