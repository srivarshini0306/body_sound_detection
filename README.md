# Cardio–Pulmonary Disease Detection System

An AI-powered system for detecting heart and lung diseases from audio recordings.

## Project Structure

- `backend/`: FastAPI server for processing audio and making predictions.
- `frontend/`: React-based web interface.
- `app.py`: Streamlit dashboard for data visualization and analysis.
- `docker/`: Docker configuration for containerized deployment.

## Getting Started

### Prerequisites

- Docker and Docker Compose (recommended)
- Python 3.10+
- Node.js 20+

### Running with Docker

1.  Clone the repository.
2.  Navigate to the project root.
3.  Run the following command:
    ```bash
    docker-compose -f docker/docker-compose.yml up --build
    ```
4.  Access the services:
    - **FastAPI API**: [http://localhost:8000](http://localhost:8000)
    - **Streamlit Dashboard**: [http://localhost:8501](http://localhost:8501)

### Manual Installation

#### Backend
1.  Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the FastAPI server:
    ```bash
    uvicorn main:app --reload
    ```

#### Frontend
1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Run the development server:
    ```bash
    npm run dev
    ```

## CI/CD Pipeline

The project includes a GitLab CI/CD pipeline configured in `.gitlab-ci.yml`. It handles:
- **Build**: Building Docker images for backend and dashboard.
- **Test**: Linting and running automated tests.
- **Deploy**: Staging deployment (placeholder).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


537615204331.dkr.ecr.ap-south-1.amazonaws.com/cancerdetection
