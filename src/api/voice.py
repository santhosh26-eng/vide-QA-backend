import base64
import io
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse

from src.llm.generator import generate_answer
from src.retrieval.retriever import retrieve_chunks
from src.speech.stt import speech_to_text
from src.speech.tts import text_to_speech
from src.utils.logger import logger

router = APIRouter(
    prefix="/voice",
    tags=["Voice"]
)


@router.post("/")
async def voice_chat(
    file: UploadFile = File(...),
    video_id: str = Form(None)
):
    """Accept voice input, transcribe it, answer it, and return spoken output."""

    temp_path = None

    try:
        logger.info("Received voice chat request")

        suffix = Path(file.filename or "recording.wav").suffix or ".wav"
        with NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            temp_path = Path(tmp.name)
            tmp.write(await file.read())

        logger.info(f"Saved uploaded voice file to: {temp_path}")

        question = speech_to_text(str(temp_path))
        logger.info(f"Transcribed voice question: {question}")

        if not question or not question.strip():
            question = "Could you please summarize the video?"

        chunks = await retrieve_chunks(question, video_id=video_id)
        answer_text = generate_answer(question, chunks)
        logger.info(f"Generated voice answer text: {answer_text}")

        spoken_audio = text_to_speech(answer_text)

        # Base64-encode headers to safely transmit UTF-8 question & answer text
        headers = {
            "X-Transcribed-Question-B64": base64.b64encode(question.encode("utf-8")).decode("ascii"),
            "X-Answer-Text-B64": base64.b64encode(answer_text.encode("utf-8")).decode("ascii"),
        }

        return StreamingResponse(
            io.BytesIO(spoken_audio),
            media_type="audio/wav",
            headers=headers
        )

    except Exception as e:
        logger.exception("Error in voice chat endpoint")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if temp_path is not None and temp_path.exists():
            try:
                temp_path.unlink()
            except Exception:
                pass
