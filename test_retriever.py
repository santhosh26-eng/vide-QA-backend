import asyncio
from src.retrieval.retriever import retrieve_chunks

async def main():
    question = "What is Python?"
    chunks = await retrieve_chunks(question)

    print("\nRetrieved Chunks:\n")
    for i, chunk in enumerate(chunks, start=1):
        print(f"Chunk {i}:")
        print(chunk)
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(main())