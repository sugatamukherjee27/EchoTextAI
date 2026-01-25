<<<<<<< HEAD
import os
import shutil
import logging
import whisper

logger = logging.getLogger(__name__)

# Load model ONCE
_whisper_model = None

def _ensure_ffmpeg():
    if shutil.which("ffmpeg") is None:
        raise EnvironmentError("ffmpeg is not installed or not found in PATH.")

def _get_whisper_model():
    global _whisper_model
    if _whisper_model is None:
        _ensure_ffmpeg()
        logger.info("Loading whisper model 'tiny'...")
        _whisper_model = whisper.load_model("tiny")
    return _whisper_model


# Flask calls this
def convert_to_text(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    model = _get_whisper_model()
    logger.info("Transcribing: %s", file_path)

    # Faster + lower memory
    result = model.transcribe(
        file_path,
        fp16=False,
        verbose=False
    )

    return result["text"].strip()
=======
import os
import shutil
import logging
import whisper

logger = logging.getLogger(__name__)

# Load model ONCE
_whisper_model = None

def _ensure_ffmpeg():
    if shutil.which("ffmpeg") is None:
        raise EnvironmentError("ffmpeg is not installed or not found in PATH.")

def _get_whisper_model(model_size="tiny"):
    global _whisper_model
    if _whisper_model is None:
        _ensure_ffmpeg()
        logger.info(f"Loading whisper model '{model_size}'...")
        _whisper_model = whisper.load_model(model_size)
    return _whisper_model


# Flask calls this
def convert_to_text(file_path, model_size="tiny"):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    model = _get_whisper_model(model_size)
    logger.info("Transcribing: %s", file_path)

    # Faster + lower memory
    result = model.transcribe(
        file_path,
        fp16=False,
        verbose=False
    )

    return result["text"].strip()
>>>>>>> 1b2791f (Your descriptive commit message here)
