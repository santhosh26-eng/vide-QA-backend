import numpy as np
from src.database.mongodb import db
from src.utils.logger import logger

embedding_collection = db["embeddings"]


async def save_embeddings(video_id, embeddings):
    """
    Save all chunk embeddings into MongoDB.
    """

    documents = []

    for item in embeddings:

        documents.append(
            {
                "video_id": video_id,
                "chunk_id": item["id"],
                "text": item["text"],
                "embedding": item["embedding"]
            }
        )

    await embedding_collection.insert_many(documents)

    return True


async def search_embeddings(query_embedding, video_id=None, top_k=3):
    """
    Search for the most similar embeddings in MongoDB using cosine similarity.
    """

    logger.info(f"Searching MongoDB embeddings for video_id: {video_id}")

    # Fetch embeddings for this video or all if not specified
    query_filter = {"video_id": video_id} if video_id else {}
    cursor = embedding_collection.find(
        query_filter,
        {"text": 1, "embedding": 1, "_id": 0}
    )

    documents = await cursor.to_list(length=None)

    if not documents:
        logger.warning(f"No embeddings found for video_id: {video_id}")
        return []

    # Calculate cosine similarity for each document
    query_vec = np.array(query_embedding)

    scored_docs = []

    for doc in documents:
        doc_vec = np.array(doc["embedding"])

        # Cosine similarity
        similarity = np.dot(query_vec, doc_vec) / (
            np.linalg.norm(query_vec) * np.linalg.norm(doc_vec)
        )

        scored_docs.append({
            "text": doc["text"],
            "score": float(similarity)
        })

    # Sort by similarity (descending) and return top_k
    scored_docs.sort(key=lambda x: x["score"], reverse=True)

    top_results = scored_docs[:top_k]

    logger.info(f"Found {len(top_results)} relevant chunks.")

    return [doc["text"] for doc in top_results]