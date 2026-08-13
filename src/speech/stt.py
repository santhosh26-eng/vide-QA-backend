from pathlib import Path

from faster_whisper import WhisperModel

# Load Whisper model once
model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

# Base directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Voice uploads folder
VOICE_UPLOADS = BASE_DIR / "voice_uploads"
VOICE_UPLOADS.mkdir(exist_ok=True)


def speech_to_text(audio_path: str) -> str:
    """
    Convert speech audio to text using Faster Whisper.
    """

    segments, _ = model.transcribe(audio_path)

    question = ""

    for segment in segments:
        question += segment.text + " "

    return question.strip()