from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def find_relevant_chunks(query_embedding, chunk_embeddings, chunks, top_k=3):
    """Returns the top_k most relevant chunks based on cosine similarity."""
    chunk_embeddings = np.array(chunk_embeddings)
    scores = np.dot(chunk_embeddings, query_embedding) / (
        np.linalg.norm(chunk_embeddings, axis=1) * np.linalg.norm(query_embedding)
    )
    # Get indices of top scoring chunks
    top_idxs = scores.argsort()[-top_k:][::-1]
    return [chunks[i] for i in top_idxs]

def chunk_text(text: str, chunk_size: int = 500) -> list[str]:
    # Simple fixed-size chunking for example purposes
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def embed_text_chunks(chunks: list[str]):
    # Returns a numpy array of embeddings
    embeddings = model.encode(chunks)
    return embeddings
