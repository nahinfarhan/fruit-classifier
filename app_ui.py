import streamlit as st
import requests
from PIL import Image
import io
import cv2
import numpy as np
import time

st.set_page_config(page_title="Fruit Classifier", page_icon="🍎")

st.title("🍎 Fresh vs Rotten Fruit Classifier")

# Mode selection
mode = st.radio("Choose classification mode:", ["📁 Upload Image", "📹 Live Camera Feed"])

if mode == "📁 Upload Image":
    st.write("Upload an image to classify the fruit type and freshness")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Make prediction
        if st.button("Classify"):
            with st.spinner("Analyzing image..."):
                try:
                    # Prepare file for API request
                    uploaded_file.seek(0)
                    files = {'file': uploaded_file}
                    
                    # Call Flask API
                    response = requests.post('http://localhost:5000/predict', files=files)
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Display results
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("🍓 Fruit Type")
                            st.success(f"**{result['fruit_class'].title()}**")
                            st.write(f"Confidence: {result['fruit_confidence']:.2%}")
                        
                        with col2:
                            st.subheader("✨ Freshness")
                            if result['freshness'] == 'Fresh':
                                st.success(f"**{result['freshness']}**")
                            else:
                                st.error(f"**{result['freshness']}**")
                            st.write(f"Rotten probability: {result['freshness_prob']:.2%}")
                    
                    else:
                        st.error(f"Error: {response.json().get('error', 'Unknown error')}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to the API. Make sure the Flask server is running.")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

else:  # Live Camera Feed mode
    st.write("Use your camera to classify fruits in real-time")
    
    # Camera controls
    col1, col2 = st.columns(2)
    with col1:
        start_camera = st.button("📹 Start Camera")
    with col2:
        stop_camera = st.button("⏹️ Stop Camera")
    
    # Initialize session state
    if 'camera_active' not in st.session_state:
        st.session_state.camera_active = False
    
    if start_camera:
        st.session_state.camera_active = True
    if stop_camera:
        st.session_state.camera_active = False
    
    if st.session_state.camera_active:
        # Create placeholders for live feed
        frame_placeholder = st.empty()
        result_placeholder = st.empty()
        
        try:
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                st.error("Cannot access camera. Please check camera permissions.")
            else:
                while st.session_state.camera_active:
                    ret, frame = cap.read()
                    if not ret:
                        st.error("Failed to capture frame")
                        break
                    
                    # Convert BGR to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    # Display frame
                    frame_placeholder.image(frame_rgb, caption="Live Feed", use_column_width=True)
                    
                    # Process frame for prediction
                    img_pil = Image.fromarray(frame_rgb)
                    img_resized = img_pil.resize((224, 224))
                    
                    # Convert to bytes for API
                    img_bytes = io.BytesIO()
                    img_resized.save(img_bytes, format='JPEG')
                    img_bytes.seek(0)
                    
                    try:
                        # Send to API
                        files = {'file': img_bytes}
                        response = requests.post('http://localhost:5000/predict', files=files, timeout=1)
                        
                        if response.status_code == 200:
                            result = response.json()
                            
                            # Display results
                            with result_placeholder.container():
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.metric("🍓 Fruit Type", result['fruit_class'].title(), 
                                             f"{result['fruit_confidence']:.1%} confidence")
                                with col2:
                                    freshness_color = "normal" if result['freshness'] == 'Fresh' else "inverse"
                                    st.metric("✨ Freshness", result['freshness'], 
                                             f"{result['freshness_prob']:.1%} rotten prob")
                    
                    except requests.exceptions.RequestException:
                        result_placeholder.warning("API connection timeout - continuing...")
                    
                    # Small delay to prevent overwhelming the API
                    time.sleep(0.5)
                
            cap.release()
            
        except Exception as e:
            st.error(f"Camera error: {str(e)}")
            st.session_state.camera_active = False

# Instructions
with st.expander("ℹ️ How to use"):
    if mode == "📁 Upload Image":
        st.write("""
        1. Upload an image of a fruit (apple, banana, orange, etc.)
        2. Click 'Classify' to get predictions
        3. View the fruit type and freshness results
        
        **Supported formats:** JPG, JPEG, PNG
        """)
    else:
        st.write("""
        1. Click 'Start Camera' to begin live feed
        2. Point camera at fruits for real-time classification
        3. Results update automatically every 0.5 seconds
        4. Click 'Stop Camera' to end the session
        
        **Requirements:** Working webcam and camera permissions
        """)