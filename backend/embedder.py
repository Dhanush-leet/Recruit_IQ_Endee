from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_BASE_URL, EMBED_MODEL
import hashlib

_client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)

def embed(text: str) -> list:
    """Embed a single string. Returns normalized float vector."""
    response = _client.embeddings.create(
        model=EMBED_MODEL,
        input=text.strip()[:4096],   # Together AI token limit
    )
    return response.data[0].embedding


def embed_batch(texts: list) -> list:
    """Embed multiple strings in one API call for efficiency."""
    response = _client.embeddings.create(
        model=EMBED_MODEL,
        input=[t.strip()[:4096] for t in texts],
    )
    return [d.embedding for d in response.data]


def make_id(text: str) -> str:
    """Deterministic 16-char MD5 ID from content hash."""
    return hashlib.md5(text.encode()).hexdigest()[:16]
