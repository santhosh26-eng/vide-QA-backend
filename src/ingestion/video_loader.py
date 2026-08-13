from pathlib import Path
import shutil
from fastapi import UploadFile

# Allowed video formats
ALLOWED_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv"}

# Upload directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


def validate_video(file: UploadFile):
    """
    Validate uploaded video file.
    """
    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file format: {extension}. "
            f"Allowed formats: {', '.join(ALLOWED_EXTENSIONS)}"
        )


def save_video(file: UploadFile) -> str:
    """
    Save uploaded video to uploads folder.
    """
    validate_video(file)

    destination = UPLOAD_DIR / file.filename

    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return str(destination)