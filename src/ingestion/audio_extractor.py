from pathlib import Path
from moviepy import VideoFileClip

# Directory to store extracted audio
AUDIO_DIR = Path("audio")
AUDIO_DIR.mkdir(exist_ok=True)

def extract_audio(video_path: str) -> str:
    """
    Extract audio from a video and save it as WAV.
    """
    video_path = Path(video_path)
    audio_path = AUDIO_DIR / f"{video_path.stem}.wav"

    video = VideoFileClip(str(video_path))

    video.audio.write_audiofile(
        str(audio_path),
        fps=16000
    )

    video.close()

    return str(audio_path)