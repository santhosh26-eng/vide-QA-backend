from fastapi import APIRouter, HTTPException

from src.database.video_db import (
    get_all_videos,
    get_video_by_id,
)

router = APIRouter(
    prefix="/videos",
    tags=["Videos"]
)


@router.get("/")
async def list_videos():
    return await get_all_videos()


@router.get("/{video_id}")
async def get_video(video_id: str):

    video = await get_video_by_id(video_id)

    if not video:
        raise HTTPException(
            status_code=404,
            detail="Video not found."
        )

    return video