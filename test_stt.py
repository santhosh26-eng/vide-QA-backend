from pathlib import Path

from src.speech.stt import speech_to_text
from src.speech.tts import text_to_speech


def test_voice_round_trip():
    question_text = "Hello, please tell me what day it is."

    audio_bytes = text_to_speech(question_text)
    assert audio_bytes, "TTS should produce audio bytes"

    test_audio_path = Path("voice_test.wav")
    test_audio_path.write_bytes(audio_bytes)

    transcript = speech_to_text(str(test_audio_path))
    assert transcript, "STT should return text from audio"
    print("Transcribed text:", transcript)


if __name__ == "__main__":
    test_voice_round_trip()
