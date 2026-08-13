from src.database.mongodb import db


def get_all_videos():
    videos = list(
        db.videos.find(
            {},
            {
                "_id": 1,
                "filename": 1,
                "uploaded_at": 1
            }
        )
    )

    for video in videos:
        video["_id"] = str(video["_id"])

    return videos