import os
import requests
import logging

logger = logging.getLogger(__name__)

# Use a fast Whisper model via HF API
API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"
token = os.getenv("HF_API_KEY")
headers = {"Authorization": f"Bearer {token}"}

def _get_whisper_model(model_name="tiny"):
    """
    Placeholder to prevent app.py from breaking.
    The API handles model loading on Hugging Face's servers.
    """
    return None

def convert_to_text(file_path):
    """
    Sends audio/video file to Hugging Face for transcription.
    """
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        
        response = requests.post(API_URL, headers=headers, data=data, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        return result.get("text", "Transcription empty.")
        
    except Exception as e:
        logger.error(f"HF Transcription Error: {e}")
        return "Error during transcription API call."