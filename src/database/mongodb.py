from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings

# Create MongoDB client
client = AsyncIOMotorClient(settings.mongodb_url)

# Select database
db = client[settings.database_name]