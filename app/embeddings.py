from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def chunk_text(text: str, chunk_size: int = 500) -> list[str]:
    # Simple fixed-size chunking (can refine later)
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def embed_text_chunks(chunks: list[str]) -> list:
    return model.encode(chunks).tolist()  # Convert numpy array to list for JSON serialization if needed
