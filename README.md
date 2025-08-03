# Fresh vs Rotten Fruit Classifier

A web application for classifying fruit types and freshness using a pre-trained ResNet152 model.

## Features

- **Fruit Classification**: Identifies fruit types (apple, banana, orange, etc.)
- **Freshness Detection**: Determines if fruit is fresh or rotten
- **Web Interface**: User-friendly Streamlit UI
- **Live Camera Feed**: Real-time classification using webcam
- **REST API**: Flask backend for programmatic access
- **Docker Support**: Containerized deployment

## Quick Start

### Option 1: Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run both Flask API and Streamlit UI
python run_local.py
```

### Option 2: Docker
```bash
# Build and run with Docker Compose
docker-compose up --build
```

📖 **For detailed Docker instructions, see [DOCKER_GUIDE.md](DOCKER_GUIDE.md)**

## Access Points

### Local Development
- **Streamlit UI**: http://localhost:8501
- **Flask API**: http://localhost:5000
- **Health Check**: http://localhost:5000/health

### Docker Deployment
- **Streamlit UI**: http://localhost:8502
- **Flask API**: http://localhost:5001
- **Health Check**: http://localhost:5001/health

## API Usage

```bash
curl -X POST -F "file=@your_image.jpg" http://localhost:5000/predict
```

## Model Requirements

- Input: 224x224 RGB images
- Output: Fruit class probabilities + freshness probability
- Format: `.keras` model file named `multi_task_resnet152.keras`

**Note**: The trained model file (`multi_task_resnet152.keras`) is not included in this repository due to GitHub's file size limits. You need to:
1. Train your own model using the architecture described
2. Place the trained model file in the project root
3. Ensure it's named `multi_task_resnet152.keras`

## Camera Requirements

- Working webcam/camera device
- Camera permissions enabled for the browser/application
- Good lighting for optimal fruit detection
