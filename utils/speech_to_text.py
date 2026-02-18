import os
import shutil
import logging
import whisper
import threading

logger = logging.getLogger(__name__)

_whisper_model = None
_model_loading = False


def _ensure_ffmpeg():
    if shutil.which("ffmpeg") is None:
        raise EnvironmentError("ffmpeg is not installed or not found in PATH.")


def _load_model_async(model_name):
    global _whisper_model, _model_loading
    try:
        logger.info(f"Loading whisper model '{model_name}'...")
        _ensure_ffmpeg() 
        _whisper_model = whisper.load_model(model_name)
        logger.info("Whisper model loaded successfully.")
    except Exception as e:
        logger.error(f"Model load failed: {e}")
    finally:
        _model_loading = False


def _get_whisper_model(model_name="tiny"):
    global _whisper_model, _model_loading

    if _whisper_model is None:
        if not _model_loading:
            _model_loading = True
            threading.Thread(
                target=_load_model_async,
                args=(model_name,),
                daemon=True
            ).start()

        raise RuntimeError("Model is warming up. Try again in a few seconds.")

    return _whisper_model


def convert_to_text(file_path, model_name="tiny"):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    model = _get_whisper_model(model_name)

    logger.info("Transcribing: %s", file_path)

    result = model.transcribe(
        file_path,
        fp16=False,
        verbose=False
    )

    return result["text"].strip()
