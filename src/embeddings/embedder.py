import json
from pathlib import Path

from src.llm.embedding import get_embedding


def generate_embeddings(chunk_path):
    with open(chunk_path, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    embedding_data = []

    for chunk in chunks:

        embedding = get_embedding(chunk["text"])

        embedding_data.append(
            {
                "id": chunk["id"],
                "text": chunk["text"],
                "embedding": embedding
            }
        )

    output_dir = Path("embeddings")
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / f"{Path(chunk_path).stem}.json"

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(embedding_data, file, indent=4)

    return str(output_path)