import sys
import os
import json
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List

# Add Endee project to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(project_root, "endee", "recruitiq"))

# Import existing logic
try:
    from retrieval.matcher import find_matching_resumes
    from retrieval.scorer import compute_skill_gap, combined_score
    from ingest.embedder import embed
except ImportError:
    # Fallback/Mock logic for standalone testing
    def find_matching_resumes(*args, **kwargs): return []
    def compute_skill_gap(*args, **kwargs): return {"match_pct": 0, "matched": [], "missing": []}
    def combined_score(*args, **kwargs): return 0
    def embed(text): return [0.0] * 384

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
async def search(query: str = Form(...), top_k: int = 5, min_exp: int = 0):
    # 1. Embed query
    query_vec = embed(query)
    
    # 2. Heuristic: extract common technical keywords from query for skill gap
    # In a real app, use an LLM for this.
    common_skills = ["python", "javascript", "react", "node", "aws", "docker", "kubernetes", "ml", "ai", "sql", "tensorflow", "pytorch"]
    required_skills = [s for s in common_skills if s in query.lower()]
    if not required_skills:
        required_skills = ["general technical"]

    # 3. Search Endee
    results = find_matching_resumes(query_vec, top_k=top_k, min_exp=min_exp)
    
    # 4. Format for Frontend with additional metrics
    formatted = []
    for r in results:
        meta = r.get("metadata", {})
        sem_score = r.get("score", 0)
        
        # Compute skill gap
        candidate_skills = meta.get("skills", [])
        gap = compute_skill_gap(required_skills, candidate_skills)
        
        # Compute exp score (normalized to 0-1)
        exp_val = meta.get("years_exp", 0)
        exp_score = min(exp_val / 10, 1.0)
        
        # Combined score
        final_score = combined_score(sem_score, gap["score"], exp_score)
        
        formatted.append({
            "id": r.get("id"),
            "name": meta.get("name", "Unknown Candidate"),
            "role": meta.get("role", "Technician"),
            "location": meta.get("location", "Remote"),
            "score": int(final_score * 100),
            "semantic_score": int(sem_score * 100),
            "skill_match": gap["match_pct"],
            "skills": candidate_skills,
            "matched_skills": gap["matched"],
            "missing_skills": gap["missing"],
            "exp": f"{exp_val} years",
            "fitReason": "High semantic overlap with job requirements." if final_score > 0.7 else "Partial match with some skill gaps."
        })
    
    # If no results from DB, return empty list (frontend handles fallbacks)
    return formatted

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

