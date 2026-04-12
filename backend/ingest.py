import fitz           # PyMuPDF
import re
from embedder import embed, make_id
from endee_client import upsert_resume, upsert_batch
from config import BATCH_SIZE

SKILL_KEYWORDS = [
    "python", "java", "javascript", "typescript", "sql", "machine learning",
    "deep learning", "nlp", "docker", "kubernetes", "aws", "gcp", "azure",
    "react", "fastapi", "pytorch", "tensorflow", "langchain", "rag",
    "vector database", "system design", "go", "rust", "c++", "redis",
    "node.js", "django", "flask", "spring", "mongodb", "postgresql",
    "spark", "kafka", "airflow", "mlops", "llm", "openai", "hugging face",
    "data engineering", "data science", "devops", "ci/cd", "terraform",
]


def extract_text(pdf_bytes: bytes) -> str:
    """Extract all text from a PDF file bytes."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    return "\n".join(page.get_text() for page in doc)


def parse_metadata(text: str, filename: str) -> dict:
    """Parse resume text into structured metadata for Endee storage."""
    email  = re.findall(r'[\w.+-]+@[\w-]+\.[a-z]{2,}', text)
    skills = [s for s in SKILL_KEYWORDS if s.lower() in text.lower()]
    years  = re.findall(r'(\d+)\+?\s*years?', text.lower())
    phone  = re.findall(r'\+?[\d\s\-\(\)]{10,15}', text)
    name   = filename.replace(".pdf", "").replace("_", " ").replace("-", " ").title()
    return {
        "name":      name,
        "email":     email[0] if email else "unknown",
        "phone":     phone[0].strip() if phone else "unknown",
        "skills":    skills,
        "years_exp": int(years[0]) if years else 0,
        "location":  "India",
        "raw_text":  text[:1500],
        "filename":  filename,
    }


def ingest_resume(pdf_bytes: bytes, filename: str) -> dict:
    """Full pipeline: PDF → text → embed → upsert to Endee."""
    text = extract_text(pdf_bytes)
    meta = parse_metadata(text, filename)
    vec  = embed(text[:2000])         # embed first 2000 chars (most relevant for ranking)
    vid  = make_id(filename + text[:100])
    upsert_resume(vid, vec, meta)
    return {
        "id":           vid,
        "name":         meta["name"],
        "skills_found": len(meta["skills"]),
        "years_exp":    meta["years_exp"],
    }


def ingest_bulk(files: list) -> dict:
    """Batch ingest multiple resumes for speed (BATCH_SIZE upserts at a time)."""
    vectors, results = [], []
    for pdf_bytes, filename in files:
        text = extract_text(pdf_bytes)
        meta = parse_metadata(text, filename)
        vec  = embed(text[:2000])
        vid  = make_id(filename + text[:100])
        vectors.append({
            "id":     vid,
            "vector": vec,
            "metadata": {
                **meta,
                "skills": ",".join(meta["skills"])   # flatten to string for Endee
            }
        })
        results.append({"id": vid, "name": meta["name"]})
        if len(vectors) >= BATCH_SIZE:
            upsert_batch(vectors)
            vectors = []
    if vectors:
        upsert_batch(vectors)
    return {"ingested": len(results), "candidates": results}
