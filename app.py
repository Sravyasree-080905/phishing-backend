import os
import joblib
import gradio as gr
import pandas as pd
from ML.feature_extractor import extract_features  # HF-safe import

# Load model once
MODEL_PATH = os.path.join("ML", "phishing_model.pkl")
model = joblib.load(MODEL_PATH)

def check_url(url):
    if not url:
        return "❌ Please enter a URL"

    try:
        features = extract_features(url)
        X = pd.DataFrame([features])
        prediction = model.predict(X)[0]

        return "⚠️ Phishing Website" if prediction == 1 else "✅ Legitimate Website"

    except Exception as e:
        return f"Error: {str(e)}"

# Gradio Interface
interface = gr.Interface(
    fn=check_url,
    inputs=gr.Textbox(label="Enter URL", placeholder="https://example.com"),
    outputs=gr.Textbox(label="Result"),
    title="Phishing URL Detection System",
    description="AI-based phishing detection using Machine Learning"
)

# HF Spaces uses server_name="0.0.0.0" and server_port=7860 automatically
interface.launch()
