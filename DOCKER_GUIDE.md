# Docker Deployment Guide

## Prerequisites
- Docker installed on your system
- Docker Compose installed

## Quick Start

### 1. Build and Run with Docker Compose
```bash
# Clone the repository
git clone <repository-url>
cd ML_Project

# Build and start containers
docker-compose up --build

# Run in background (detached mode)
docker-compose up -d --build
```

### 2. Access the Application
- **Streamlit UI**: http://localhost:8502
- **Flask API**: http://localhost:5001
- **Health Check**: http://localhost:5001/health

### 3. Stop the Application
```bash
# Stop containers
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Manual Docker Commands

### Build Image
```bash
docker build -t fruit-classifier .
```

### Run Container
```bash
docker run -p 5001:5000 -p 8502:8501 fruit-classifier
```

### Run in Background
```bash
docker run -d -p 5001:5000 -p 8502:8501 --name fruit-app fruit-classifier
```

## API Usage Examples

### Test Health Endpoint
```bash
curl http://localhost:5001/health
```

### Predict with Image
```bash
curl -X POST -F "file=@path/to/your/image.jpg" http://localhost:5001/predict
```

## Troubleshooting

### Port Conflicts
If ports 5001 or 8502 are in use, modify `docker-compose.yml`:
```yaml
ports:
  - "5002:5000"  # Change external port
  - "8503:8501"  # Change external port
```

### View Logs
```bash
# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View specific service logs
docker-compose logs fruit-classifier
```

### Container Management
```bash
# List running containers
docker ps

# Stop specific container
docker stop <container-name>

# Remove container
docker rm <container-name>

# Remove image
docker rmi fruit-classifier
```

## Model Requirements
- Place your trained model file `multi_task_resnet152.keras` in the project root
- Model should accept 224x224x3 RGB images
- Model should output fruit classification and freshness probabilities