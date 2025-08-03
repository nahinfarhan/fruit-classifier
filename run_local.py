import subprocess
import time
import sys
from threading import Thread

def run_flask():
    """Run Flask API"""
    subprocess.run([sys.executable, "app.py"])

def run_streamlit():
    """Run Streamlit UI"""
    time.sleep(2)  # Wait for Flask to start
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app_ui.py"])

if __name__ == "__main__":
    print("Starting Flask API and Streamlit UI...")
    
    # Start Flask in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Start Streamlit in main thread
    run_streamlit()