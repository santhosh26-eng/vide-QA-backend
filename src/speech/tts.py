from pathlib import Path
from tempfile import NamedTemporaryFile

import pyttsx3


def text_to_speech(text: str) -> bytes:
    """Convert text to WAV audio bytes using pyttsx3."""

    with NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        temp_path = Path(tmp.name)

    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        engine.setProperty("volume", 1.0)

        voices = engine.getProperty("voices")
        if voices:
            engine.setProperty("voice", voices[0].id)

        engine.save_to_file(text, str(temp_path))
        engine.runAndWait()

        return temp_path.read_bytes()

    finally:
        if temp_path.exists():
            temp_path.unlink()
