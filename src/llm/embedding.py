import sys
from pathlib import Path

# Ensure backend root is in sys.path when executed directly
backend_root = Path(__file__).resolve().parent.parent.parent
if str(backend_root) not in sys.path:
    sys.path.insert(0, str(backend_root))

import google.generativeai as genai
from src.core.config import settings

genai.configure(api_key=settings.gemini_api_key)


def get_embedding(text: str):
    """
    Generate embedding using Gemini.
    """

    result = genai.embed_content(
        model="models/gemini-embedding-001",
        content=text
    )

    return result["embedding"]


if __name__ == "__main__":
    sample_text = "What is Multimodal RAG?"
    print(f"Generating embedding for: '{sample_text}'...")
    embedding = get_embedding(sample_text)
    print(f"Embedding generated successfully!")
    print(f"Vector dimension: {len(embedding)}")
    print(f"Sample values (first 5): {embedding[:5]}")