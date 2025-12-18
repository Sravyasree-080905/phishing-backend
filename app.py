import joblib
import gradio as gr
import pandas as pd
import os
import sys

# Allow imports from ML folder
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from ML.feature_extractor import extract_features

# Load model once
model = joblib.load("ML/phishing_model.pkl")

def check_url(url):
    if not url:
        return "❌ Please enter a URL"

    try:
        features = extract_features(url)
        X = pd.DataFrame([features])
        prediction = model.predict(X)[0]

        if prediction == 1:
            return "⚠️ Phishing Website"
        else:
            return "✅ Legitimate Website"

    except Exception as e:
        return f"Error: {str(e)}"

interface = gr.Interface(
    fn=check_url,
    inputs=gr.Textbox(label="Enter URL"),
    outputs=gr.Textbox(label="Result"),
    title="Phishing URL Detection System",
    description="AI-based phishing detection using Machine Learning"
)

interface.launch()
