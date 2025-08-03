import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(page_title="Fruit Classifier", page_icon="🍎")

st.title("🍎 Fresh vs Rotten Fruit Classifier")
st.write("Upload an image to classify the fruit type and freshness")

# File uploader
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

# Instructions
with st.expander("ℹ️ How to use"):
    st.write("""
    1. Upload an image of a fruit (apple, banana, orange, etc.)
    2. Click 'Classify' to get predictions
    3. View the fruit type and freshness results
    
    **Supported formats:** JPG, JPEG, PNG
    """)