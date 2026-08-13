from src.database.embedding_db import search_embeddings
from src.llm.embedding import get_embedding
from src.utils.logger import logger


async def retrieve_chunks(query: str, video_id: str = None, top_k: int = 3):
    """
    Retrieve the most relevant transcript chunks for a given video.
    """

    try:
        logger.info("=" * 60)
        logger.info("Retriever Started")
        logger.info(f"Question : {query}")
        logger.info(f"Video ID : {video_id}")

        # Generate embedding using Gemini
        logger.info("Generating query embedding using Gemini...")

        query_embedding = get_embedding(query)

        logger.info("Query embedding generated successfully.")

        # Search MongoDB embeddings
        documents = await search_embeddings(query_embedding, video_id, top_k)

        logger.info(f"Retrieved {len(documents)} relevant chunks.")

        for index, chunk in enumerate(documents, start=1):
            logger.info(f"Chunk {index}: {chunk[:100]}...")

        logger.info("Retriever Completed")
        logger.info("=" * 60)

        return documents

    except Exception:
        logger.exception("Retriever Error")
        raise