# Camera Setup Guide

## Docker Limitations

**Important**: Docker containers cannot access the host camera directly on macOS. The live camera feed feature requires local execution.

## Solutions

### Option 1: Local Execution (Recommended for Camera)
```bash
# Stop Docker if running
docker-compose down

# Run locally with camera access
python run_local.py
```

**Access Points:**
- Streamlit UI: http://localhost:8501
- Flask API: http://localhost:5000

### Option 2: Docker (Image Upload Only)
```bash
# Run Docker for image upload functionality
docker-compose up -d
```

**Access Points:**
- Streamlit UI: http://localhost:8502
- Flask API: http://localhost:5001

**Note**: Live camera feed will show "Cannot access camera" in Docker.

## Camera Permissions

### macOS
1. Go to System Preferences > Security & Privacy > Camera
2. Enable camera access for Terminal/Python
3. Restart the application if needed

### Browser Permissions
1. When prompted, allow camera access
2. Check browser settings if camera is blocked
3. Use Chrome/Firefox for best compatibility

## Troubleshooting

- **"Cannot access camera"**: Run locally instead of Docker
- **"Permission denied"**: Check system camera permissions
- **"Camera in use"**: Close other applications using camera
- **Black screen**: Try different camera indices (0, 1, 2)