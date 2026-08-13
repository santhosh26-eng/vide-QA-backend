from pathlib import Path
import json
from faster_whisper import WhisperModel

# Folder to store transcripts
TRANSCRIPT_DIR = Path("transcripts")
TRANSCRIPT_DIR.mkdir(exist_ok=True)

# Load Whisper model (loaded once when the module is imported)
model = WhisperModel(
    "tiny",
    device="cpu",
    compute_type="int8",
    download_root="./models"
)


def transcribe_audio(audio_path: str) -> str:
    """
    Transcribe audio and save transcript as JSON.
    Returns the transcript file path.
    """

    audio_path = Path(audio_path)

    transcript_path = TRANSCRIPT_DIR / f"{audio_path.stem}.json"

    segments, info = model.transcribe(str(audio_path))

    transcript = []

    for segment in segments:
        transcript.append(
            {
                "start": round(segment.start, 2),
                "end": round(segment.end, 2),
                "text": segment.text.strip()
            }
        )

    with open(transcript_path, "w", encoding="utf-8") as f:
        json.dump(transcript, f, indent=4, ensure_ascii=False)

    return str(transcript_path)