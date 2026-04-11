import sys
import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List

# Add Endee project to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(project_root, "endee", "recruitiq"))

# Import existing logic (if possible, or mock if paths fail)
try:
    from retrieval.matcher import find_matching_resumes
    from retrieval.scorer import compute_skill_gap, combined_score
    from ingest.embedder import embed
except ImportError:
    # Fallback/Mock logic for standalone testing
    def find_matching_resumes(*args, **kwargs): return []
    def compute_skill_gap(*args, **kwargs): return {"match_pct": 0, "matched": [], "missing": []}
    def combined_score(*args, **kwargs): return 0
    def embed(text): return [0.0] * 1536

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "online", "database": "endee"}

@app.post("/search")
async def search(query: str = Form(...), top_k: int = 5):
    # 1. Embed query
    query_vec = embed(query)
    
    # 2. Search Endee
    results = find_matching_resumes(query_vec, top_k=top_k)
    
    # 3. Format for Frontend
    formatted = []
    for r in results:
        meta = r.get("metadata", {})
        score = int(r.get("score", 0) * 100)
        formatted.append({
            "id": r.get("id"),
            "name": meta.get("name", "Unknown Candidate"),
            "role": meta.get("role", "Technician"),
            "location": meta.get("location", "Remote"),
            "score": score,
            "skills": meta.get("skills", []),
            "exp": f"{meta.get('years_exp', 0)} years",
            "fitReason": "High semantic overlap with job requirements."
        })
    
    return formatted

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
