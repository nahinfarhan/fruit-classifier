import tensorflow as tf
from flask import Flask, request, jsonify
import numpy as np
from PIL import Image
import io

# Load the pre-trained model
try:
    model = tf.keras.models.load_model('multi_task_resnet152.keras')
except:
    print("Warning: Model file not found. Using dummy responses.")
    model = None

app = Flask(__name__)

# Fruit class names (adjust based on your model's classes)
FRUIT_CLASSES = ['apple', 'banana', 'orange', 'mixed']  # Update with your actual classes

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        # Preprocess image
        img = Image.open(io.BytesIO(file.read()))
        img = img.convert('RGB')
        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        if model is None:
            # Dummy predictions when model is not available
            import random
            fruit_class = random.choice(FRUIT_CLASSES)
            fruit_confidence = random.uniform(0.7, 0.95)
            freshness_prob = random.uniform(0.1, 0.8)
            freshness = 'Rotten' if freshness_prob > 0.5 else 'Fresh'
        else:
            # Make predictions
            predictions = model.predict(img_array)
            
            # Fruit Classification
            fruit_class_probs = predictions[0][0]
            fruit_class_idx = np.argmax(fruit_class_probs)
            fruit_class = FRUIT_CLASSES[fruit_class_idx] if fruit_class_idx < len(FRUIT_CLASSES) else f"Class_{fruit_class_idx}"
            fruit_confidence = float(np.max(fruit_class_probs))
            
            # Freshness Classification
            freshness_prob = float(predictions[1][0][0])
            freshness = 'Rotten' if freshness_prob > 0.5 else 'Fresh'

        return jsonify({
            'fruit_class': fruit_class,
            'freshness': freshness,
            'fruit_confidence': fruit_confidence if model else fruit_confidence,
            'freshness_prob': freshness_prob
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)