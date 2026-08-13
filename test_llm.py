import asyncio
from src.retrieval.retriever import retrieve_chunks
from src.llm.generator import generate_answer

async def main():
    question = "What is Generative AI?"
    chunks = await retrieve_chunks(question)
    answer = generate_answer(question, chunks)
    print("\nAnswer:\n", answer)

if __name__ == "__main__":
    asyncio.run(main())