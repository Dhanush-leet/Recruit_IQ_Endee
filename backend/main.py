from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from endee_client import setup_indexes, get_index_stats
from ingest import ingest_resume, ingest_bulk
from agent import run_search

app = FastAPI(title="RecruitIQ API", version="2.0.0", description="AI Resume Screening powered by Endee Vector DB")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    """Create Endee indexes on first run (idempotent)."""
    print("[RecruitIQ] Starting up -- connecting to Endee...")
    try:
        setup_indexes()
        print("[RecruitIQ] Ready!")
    except Exception as e:
        print(f"[RecruitIQ] Warning: Could not connect to Endee vector database at startup. ({str(e)})")


@app.get("/health")
def health_check():
    stats = get_index_stats()
    return {
        "backend":      "online",
        "endee_status": "online" if stats.get("status") == "connected" else "offline",
        "endee_port":   8080,
        "details":      stats
    }


@app.post("/upload")
@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Ingest a single PDF resume into Endee vector DB."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    content = await file.read()
    result  = ingest_resume(content, file.filename)
    return {
        "status": "success",
        "filename": file.filename,
        "message": "Resume ingested into Endee DB successfully ✅",
        **result
    }


@app.post("/upload/bulk")
async def upload_bulk(files: List[UploadFile] = File(...)):
    """Batch ingest multiple PDF resumes."""
    pairs = []
    for f in files:
        if not f.filename.lower().endswith(".pdf"):
            continue
        content = await f.read()
        pairs.append((content, f.filename))
    if not pairs:
        raise HTTPException(status_code=400, detail="No valid PDF files provided")
    from ingest import ingest_bulk
    result = ingest_bulk(pairs)
    return {"status": "bulk_indexed", **result}


class SearchRequest(BaseModel):
    jd: str
    required_skills: List[str] = []
    min_exp: int = 0
    top_k: int = 8


@app.post("/search")
def search(req: SearchRequest):
    """Run full RAG pipeline: embed JD → Endee search → composite scoring → AI analysis."""
    if not req.jd.strip():
        raise HTTPException(status_code=400, detail="Job description is required")
    results = run_search(req.jd, req.required_skills, req.min_exp, req.top_k)
    return {"count": len(results), "candidates": results}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
