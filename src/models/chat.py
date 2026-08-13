from pydantic import BaseModel
from datetime import datetime


class Chat(BaseModel):
    user_id: str
    video_id: str

    question: str
    answer: str

    timestamp: datetime = datetime.utcnow()