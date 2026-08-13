import asyncio

from src.database.mongodb import db

async def test():
    print("Program Started")

    collections = await db.list_collection_names()

    print("✅ Connected Successfully!")
    print("Collections:", collections)

if __name__ == "__main__":
    asyncio.run(test())