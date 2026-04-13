from endee import Endee, Precision
from config import ENDEE_URL, ENDEE_TOKEN, INDEX_NAME, JD_INDEX_NAME, EMBED_DIM

# ── Initialize client ──────────────────────────────────────────────
# For local Docker: token can be empty string — Endee runs open by default
client = Endee(token=ENDEE_TOKEN if ENDEE_TOKEN else "local")
client.set_base_url(ENDEE_URL)


def setup_indexes():
    """Create both indexes if they don't exist yet. Call once at startup."""
    try:
        existing = {idx["name"] for idx in (client.list_indexes() or [])}
    except Exception:
        print("[Endee] Offline - Skipping index setup")
        return

    for name in [INDEX_NAME, JD_INDEX_NAME]:
        if name not in existing:
            client.create_index(
                name=name,
                dimension=EMBED_DIM,
                space_type="cosine",        # cosine similarity — best for semantic matching
                M=16,                       # HNSW graph connectivity
                ef_con=128,                 # construction-time accuracy parameter
                precision=Precision.INT8D,  # 4x memory saving, same recall
            )
            print(f"[Endee] Created index: {name}  (dim={EMBED_DIM}, INT8D, cosine)")
        else:
            print(f"[Endee] Index already exists: {name}")


def upsert_resume(vector_id: str, vector: list, metadata: dict):
    """
    Store a resume embedding with metadata.
    metadata keys: name, email, skills (list), years_exp, location, raw_text, filename
    """
    client.upsert(
        index_name=INDEX_NAME,
        vectors=[{
            "id": vector_id,
            "vector": vector,
            "metadata": {
                **metadata,
                # Endee metadata must be flat — serialize lists to strings
                "skills": ",".join(metadata.get("skills", [])),
            }
        }]
    )


def upsert_batch(vectors: list):
    """Batch upsert for speed — use when ingesting many resumes at once."""
    client.upsert(index_name=INDEX_NAME, vectors=vectors)


def search_resumes(
    query_vector: list,
    top_k: int = 8,
    min_exp: int = 0,
) -> list:
    """
    Semantic search with optional metadata filter.
    Returns list of {id, score, metadata} dicts.
    """
    filters = {}
    if min_exp > 0:
        filters = {"years_exp": {"$gte": min_exp}}

    try:
        results = client.search(
            index_name=INDEX_NAME,
            query_vector=query_vector,
            top_k=top_k,
            filters=filters if filters else None,
            include_metadata=True,
        )
        return results or []
    except Exception as e:
        print(f"[Endee] Search failed (Offline): {e}")
        return []


def get_index_stats() -> dict:
    """Return vector count and index health."""
    try:
        indexes = client.list_indexes() or []
        resume_idx = next((i for i in indexes if i["name"] == INDEX_NAME), {})
        jd_idx = next((i for i in indexes if i["name"] == JD_INDEX_NAME), {})
        return {
            "status": "connected",
            "endee_url": ENDEE_URL,
            "resume_index": INDEX_NAME,
            "jd_index": JD_INDEX_NAME,
            "resume_vector_count": resume_idx.get("vector_count", 0),
            "jd_vector_count": jd_idx.get("vector_count", 0),
            "embed_dim": EMBED_DIM,
            "precision": "INT8D",
            "space_type": "cosine",
        }
    except Exception as e:
        return {"status": "error", "detail": str(e)}


def delete_index(name: str = INDEX_NAME):
    """Wipe and recreate the index (useful for demo resets)."""
    try:
        client.delete_index(name=name)
        print(f"[Endee] Deleted index: {name}")
    except Exception:
        pass
