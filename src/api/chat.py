from typing import Optional
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from src.retrieval.retriever import retrieve_chunks
from src.llm.generator import stream_answer
from src.utils.logger import logger

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


class ChatRequest(BaseModel):
    question: str
    video_id: Optional[str] = None


@router.post("/")
async def chat(request: ChatRequest):

    logger.info("=" * 60)
    logger.info("New Chat Request")
    logger.info(f"Video ID: {request.video_id}")
    logger.info(f"Question: {request.question}")

    chunks = await retrieve_chunks(
        request.question,
        request.video_id
    )

    if not chunks:
        raise HTTPException(
            status_code=404,
            detail="No information found for this video."
        )

    return StreamingResponse(
        stream_answer(
            request.video_id,
            request.question,
            chunks
        ),
        media_type="text/plain"
    )