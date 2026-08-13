from pydantic import BaseModel
from datetime import datetime


class Video(BaseModel):
    user_id: str
    filename: str
    transcript: str

    upload_time: datetime = datetime.utcnow()