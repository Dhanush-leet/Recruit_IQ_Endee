from sentence_transformers import SentenceTransformer
import hashlib

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed(text: str) -> list:
    return model.encode(text, normalize_embeddings=True).tolist()

def make_id(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()[:16]
