from datetime import datetime
from bson import ObjectId

from src.database.mongodb import db


chat_collection = db["chat_history"]


async def save_chat(video_id, question, answer):
    chat = {
        "video_id": ObjectId(video_id) if ObjectId.is_valid(video_id) else video_id,
        "question": question,
        "answer": answer,
        "created_at": datetime.utcnow()
    }

    result = await chat_collection.insert_one(chat)

    return str(result.inserted_id)