# NeuroDigits: Handwritten Digit Recognition Web App

NeuroDigits is a web-based application that allows users to draw digits on a canvas and predicts the drawn digit using a trained Convolutional Neural Network (CNN). 
The application is powered by Flask for the backend and TensorFlow for the ML model, with a user-friendly frontend interface.

## Features

- **Interactive Canvas**: Draw digits directly on the web interface.
- **Real-Time Predictions**: Get predictions along with confidence scores for each digit.
- **Dark Mode**: Toggle between light and dark themes for user comfort.
- **Download Functionality**: Save your drawn digit as an image file.

## Demo

🚀 **[Live Demo on Vercel](https://neuro-digits.vercel.app/)**

Click the link above to try the app live! Here's a quick preview:

### **Screenshot**
![App Screenshot](demo/Screen Recording 2025-01-01 at 11.19.27 AM.mov)

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/aaaikins/NeuroDigits.git
   cd NeuroDigits
   ```

2. **Install dependencies**:
   Ensure you have Python 3.8+ installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Train the model** (optional):
   If you'd like to train the model from scratch, execute:
   ```bash
   python train.py
   ```
   The trained model will be saved as `cnn_model.keras`.

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the app**:
   Open your browser and navigate to `http://localhost:5001`.

## Deployment

For deployment on a production server:
1. Use a production WSGI server like Gunicorn:
   ```bash
   gunicorn --bind 0.0.0.0:8000 app:app
   ```
2. Set up NGINX or Apache to serve the app and static files.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript (Canvas API)
- **Backend**: Flask
- **Machine Learning**: TensorFlow, Keras
- **Dataset**: MNIST

## Folder Structure

```
NeuroDigits/
├── app.py              # Flask app
├── train.py            # Model training script
├── static/
│   ├── styles.css      # Main styles
│   └── script.js       # Frontend logic
├── templates/
│   └── index.html      # HTML template
├── model/
│   └── cnn_model.keras # Trained model
└── README.md           # Project documentation
```
