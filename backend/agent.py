from openai import OpenAI
from embedder import embed
from endee_client import search_resumes
from config import OPENAI_API_KEY, OPENAI_BASE_URL, LLM_MODEL, TOP_K
import json, re

_llm = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)


def score_candidate(result: dict, required_skills: list) -> dict:
    """Compute composite score: 50% semantic + 35% skill match + 15% experience."""
    meta       = result.get("metadata", {})
    raw_skills = meta.get("skills", "")
    cand_skills = set(s.strip().lower() for s in raw_skills.split(",") if s.strip())
    req_set    = set(s.lower() for s in required_skills)

    matched    = req_set & cand_skills
    missing    = req_set - cand_skills
    skill_pct  = round(len(matched) / len(req_set) * 100) if req_set else 80
    sem_score  = round(result.get("score", 0) * 100)
    exp_val    = int(meta.get("years_exp", 0))
    exp_score  = min(exp_val * 12, 100)                    # 8+ yrs = 100%
    combined   = round(sem_score * 0.50 + skill_pct * 0.35 + exp_score * 0.15)

    return {
        **meta,
        "id":              result.get("id", ""),
        "skills":          list(cand_skills),
        "matched_skills":  list(matched),
        "missing_skills":  list(missing),
        "semantic_score":  sem_score,
        "skill_match":     skill_pct,
        "exp_score":       exp_score,
        "score":           combined,
    }


def screen_candidate(jd: str, candidate: dict) -> dict:
    """Call LLM to generate structured AI screening analysis."""
    prompt = f"""You are a senior technical recruiter AI.
Assess this candidate for the job description and respond ONLY with valid JSON — no markdown fences.

JOB DESCRIPTION:
{jd[:600]}

CANDIDATE:
Name: {candidate.get('name', 'Unknown')}
Skills: {', '.join(candidate.get('skills', []))}
Experience: {candidate.get('years_exp', 0)} years
Matched skills: {', '.join(candidate.get('matched_skills', []))}
Missing skills: {', '.join(candidate.get('missing_skills', []))}
Semantic match: {candidate.get('semantic_score')}%

Return EXACTLY this JSON structure:
{{
  "recommendation": "STRONG FIT | GOOD FIT | PARTIAL FIT | NOT FIT",
  "hire_reason": "2-3 sentence justification focusing on strengths",
  "concern": "1 key gap or risk to flag",
  "interview_questions": ["Question 1", "Question 2", "Question 3"]
}}"""

    try:
        resp = _llm.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=400,
        )
        raw = resp.choices[0].message.content.strip()
        raw = re.sub(r"```json|```", "", raw).strip()
        return json.loads(raw)
    except Exception as e:
        return {
            "recommendation": "PARTIAL FIT",
            "hire_reason": f"Candidate shows {candidate.get('semantic_score', 0)}% semantic match with the role requirements.",
            "concern": "AI analysis unavailable — review manually.",
            "interview_questions": [
                "Walk me through your most relevant project.",
                "How do you handle tight deadlines?",
                "What's your experience with the required tech stack?",
            ],
        }


def run_search(jd: str, required_skills: list, min_exp: int = 0, top_k: int = 8) -> list:
    """Full RAG pipeline: embed JD → Endee vector search → score → AI screen."""
    jd_vec  = embed(jd)
    raw     = search_resumes(jd_vec, top_k=top_k, min_exp=min_exp)

    results = []
    for r in raw:
        scored = score_candidate(r, required_skills)
        ai     = screen_candidate(jd, scored)
        results.append({**scored, "ai_analysis": ai})

    # Sort by composite score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    return results
