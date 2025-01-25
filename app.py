import json
from tensorflow.keras.models import load_model
from flask import Flask, render_template, request
from PIL import Image
import numpy as np
import base64
import io

app = Flask(__name__)

# Load the Keras model
model = load_model("model/cnn_model.keras")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict_digit():
    try:
        # Get the image data from the JSON request
        data = request.get_json()
        image_data = data.get('image')
        
        # Decode base64 image
        image_bytes = base64.b64decode(image_data)
        img = Image.open(io.BytesIO(image_bytes)).convert('L')
        
        # Preprocess the image
        img = img.resize((28, 28))  # Resize to 28x28
        img_array = np.array(img)
        
        # Normalize to [0, 1] and invert colors (MNIST has white digits on black background)
        img_array = 1 - (img_array / 255.0)
        
        # This helps remove grey pixels and make the digit more defined
        img_array = (img_array > 0.3).astype(np.float32)
        
        # Add required dimensions for the model
        img_array = np.expand_dims(img_array, axis=-1)
        img_array = np.expand_dims(img_array, axis=0)
        
        # Make prediction
        predictions = model.predict(img_array, verbose=0)
        predicted_class = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class])
        
        # Return prediction results
        return json.dumps({
            'predicted_label': int(predicted_class),
            'confidence': confidence * 100,  # Convert to percentage
            'probabilities': [float(p) * 100 for p in predictions[0]]  # All class probabilities
        })
        
    except Exception as e:
        return json.dumps({'error': str(e)})

if __name__ == "__main__":
    app.run()
