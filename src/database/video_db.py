from datetime import datetime
from src.database.mongodb import db

video_collection = db["videos"]


async def save_video_metadata(
    filename: str,
    video_path: str,
    transcript: str,
):
    document = {
        "filename": filename,
        "video_path": video_path,
        "transcript": transcript,
        "upload_time": datetime.utcnow(),
        "status": "Processed"
    }

    result = await video_collection.insert_one(document)

    return str(result.inserted_id)


async def get_all_videos():
    """
    Retrieve all videos from MongoDB.
    """

    cursor = video_collection.find({}, {"transcript": 0})
    videos = await cursor.to_list(length=None)

    for video in videos:
        video["_id"] = str(video["_id"])

    return videos


async def get_video_by_id(video_id: str):
    """
    Retrieve a single video by its ID.
    """

    from bson import ObjectId

    video = await video_collection.find_one({"_id": ObjectId(video_id)})

    if video:
        video["_id"] = str(video["_id"])

    return video