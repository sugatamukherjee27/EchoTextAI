import os
import requests
import time
import logging

logger = logging.getLogger(__name__)

# Recommended high-speed Whisper model
API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"
token = os.getenv("HF_API_KEY")
HEADERS = {"Authorization": f"Bearer {token}"}

def _get_whisper_model(model_name="tiny"):
    """
    Keep this stub so app.py doesn't crash during initialization.
    The model is now hosted on Hugging Face, not locally.
    """
    return None

def convert_to_text(file_path):
    """
    Sends audio to Hugging Face Inference API for transcription.
    """
    try:
        with open(file_path, "rb") as f:
            data = f.read()

        # Send request to HF API
        response = requests.post(API_URL, headers=HEADERS, data=data, timeout=120)
        
        # If the model is still loading (Status 503), wait and retry once
        if response.status_code == 503:
            time.sleep(5)
            response = requests.post(API_URL, headers=HEADERS, data=data, timeout=120)
            
        response.raise_for_status()
        result = response.json()
        
        return result.get("text", "No text found in response.")

    except Exception as e:
        logger.error(f"HF Transcription Error: {e}")
        return f"Transcription error: {str(e)}"