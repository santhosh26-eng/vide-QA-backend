import json

from fastapi import APIRouter, UploadFile, File, HTTPException

from src.database.video_db import save_video_metadata
from src.database.embedding_db import save_embeddings

from src.ingestion.video_loader import save_video
from src.ingestion.audio_extractor import extract_audio
from src.ingestion.whisper_transcriber import transcribe_audio

from src.chunking.recursive_chunker import chunk_transcript
from src.embeddings.embedder import generate_embeddings

from src.utils.logger import logger

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.post("/")
async def upload_video(file: UploadFile = File(...)):
    try:
        logger.info("=" * 60)
        logger.info("New video upload request received.")
        logger.info(f"Uploaded File: {file.filename}")

        # =====================================================
        # 1. Save Video
        # =====================================================
        logger.info("Saving uploaded video...")
        video_path = save_video(file)
        logger.info(f"Video saved successfully: {video_path}")

        # =====================================================
        # 2. Extract Audio
        # =====================================================
        logger.info("Extracting audio from video...")
        audio_path = extract_audio(video_path)
        logger.info(f"Audio extracted successfully: {audio_path}")

        # =====================================================
        # 3. Whisper Transcription
        # =====================================================
        import gc
        gc.collect()  # Force garbage collection to free up RAM before transcription

        logger.info("Starting Whisper transcription...")
        transcript_path = transcribe_audio(audio_path)
        logger.info(f"Transcript generated successfully: {transcript_path}")

        # =====================================================
        # 4. Read Transcript
        # =====================================================
        logger.info("Reading transcript...")

        with open(transcript_path, "r", encoding="utf-8") as transcript_file:
            transcript = transcript_file.read()

        # =====================================================
        # 5. Save Metadata to MongoDB
        # =====================================================
        logger.info("Saving metadata to MongoDB...")

        video_id = await save_video_metadata(
            filename=file.filename,
            video_path=video_path,
            transcript=transcript
        )

        logger.info(f"Metadata saved successfully. MongoDB ID: {video_id}")

        # =====================================================
        # 6. Recursive Chunking
        # =====================================================
        logger.info("Chunking transcript...")
        chunk_path = chunk_transcript(transcript_path)
        logger.info(f"Chunks created successfully: {chunk_path}")

        # =====================================================
        # 7. Generate Embeddings
        # =====================================================
        logger.info("Generating embeddings...")
        embedding_path = generate_embeddings(chunk_path)
        logger.info(f"Embeddings generated successfully: {embedding_path}")

        # =====================================================
        # 8. Store Embeddings in MongoDB
        # =====================================================
        logger.info("Storing embeddings in MongoDB...")

        with open(embedding_path, "r", encoding="utf-8") as emb_file:
            embeddings = json.load(emb_file)

        await save_embeddings(video_id, embeddings)
        logger.info("Embeddings stored successfully.")

        logger.info("Video processing completed successfully.")
        logger.info("=" * 60)

        return {
            "message": "Video processed successfully.",
            "video_id": video_id,
            "mongodb_id": video_id,
            "video_name": file.filename,
            "video_path": video_path,
            "audio_path": audio_path,
            "transcript_path": transcript_path,
            "chunk_path": chunk_path,
            "embedding_path": embedding_path
        }

    except ValueError as e:
        logger.error(f"Validation Error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        logger.exception("Unexpected error occurred while processing the video.")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )