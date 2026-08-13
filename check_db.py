import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings


async def check():
    client = AsyncIOMotorClient(settings.mongodb_url)
    db = client[settings.database_name]

    collection = db["embeddings"]

    count = await collection.count_documents({})
    print("Collection: embeddings")
    print(f"Number of Documents: {count}")

    # Show a sample document (without the full embedding vector)
    sample = await collection.find_one({}, {"embedding": 0})
    if sample:
        print(f"Sample Document: {sample}")

    client.close()


asyncio.run(check())