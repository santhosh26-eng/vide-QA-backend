from src.llm.embedding import get_embedding

sample_text = "What is Multimodal RAG?"

print(f"Generating Gemini embedding for: '{sample_text}'...")
embedding = get_embedding(sample_text)

print("\n--- Result ---")
print(f"Status: Success")
print(f"Embedding Vector Dimension: {len(embedding)}")
print(f"First 5 dimensions: {embedding[:5]}")
