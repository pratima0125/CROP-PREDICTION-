from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import pickle

# Flask app setup
app = Flask(__name__)


# Load model components
def load_model_components():
    """Load model and preprocessing components from disk"""
    try:
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('preprocessor.pkl', 'rb') as f:
            preprocessor = pickle.load(f)
        with open('label_encoder.pkl', 'rb') as f:
            label_encoder = pickle.load(f)
        return model, preprocessor, label_encoder
    except FileNotFoundError:
        raise Exception("Model components not found. Please train the model first.")


# Load model, preprocessor, and label encoder
model, preprocessor, label_encoder = load_model_components()


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/predict", methods=['POST'])
def predict():
    try:
        # Collect and convert inputs from the form
        N = float(request.form['Nitrogen'])
        P = float(request.form['Phosporus'])
        K = float(request.form['Potassium'])
        temp = float(request.form['Temperature'])
        humidity = float(request.form['Humidity'])
        ph = float(request.form['Ph'])
        rainfall = float(request.form['Rainfall'])

        # Prepare the input data for prediction
        features = pd.DataFrame([[N, P, K, temp, humidity, ph, rainfall]],
                                columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'])

        # Transform features
        transformed_features = preprocessor.transform(features)

        # Predict crop with the model
        pred_proba = model.predict_proba(transformed_features)

        # Get the most probable crop prediction
        max_prob_idx = np.argmax(pred_proba)
        crop_name = label_encoder.inverse_transform([max_prob_idx])[0]
        confidence = pred_proba[0][max_prob_idx]
        print(crop_name)
        result = f"Recommended Crop: {crop_name} (Confidence: {confidence:.2%})"
    except Exception as e:
        result = f"An error occurred: {e}"

    return render_template('index.html', result=result)


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
