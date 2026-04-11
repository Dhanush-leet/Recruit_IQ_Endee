import fitz  # PyMuPDF
import re

def extract_resume_text(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    return "\n".join(page.get_text() for page in doc)

def parse_resume_metadata(text: str, filename: str) -> dict:
    """Lightweight heuristic extraction — no external API needed"""
    email = re.findall(r'[\w.+-]+@[\w-]+\.[a-z]{2,}', text)
    skills_keywords = [
        "python","java","javascript","sql","machine learning","deep learning",
        "nlp","docker","kubernetes","aws","gcp","azure","react","fastapi",
        "pytorch","tensorflow","langchain","rag","llm","vector database"
    ]
    found_skills = [s for s in skills_keywords if s.lower() in text.lower()]
    years = re.findall(r'(\d+)\+?\s*years?', text.lower())
    
    return {
        "name": filename.replace(".pdf", "").replace("_", " ").title(),
        "email": email[0] if email else "unknown",
        "skills": found_skills,
        "years_exp": int(years[0]) if years else 0,
        "location": "India",  # default; can be extracted with spaCy
        "raw_text": text[:2000]  # first 2000 chars as context for RAG
    }
