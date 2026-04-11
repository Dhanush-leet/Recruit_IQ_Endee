def build_screening_prompt(jd_text: str, resume_text: str,
                            skill_gap: dict, semantic_score: float) -> str:
    return f"""You are a senior technical recruiter AI assistant.
Analyze this candidate's fit for the job and give a clear hiring recommendation.

JOB DESCRIPTION:
{jd_text[:800]}

CANDIDATE RESUME EXCERPT:
{resume_text[:800]}

SKILL ANALYSIS:
- Semantic match score: {round(semantic_score * 100)}%
- Skills matched: {', '.join(skill_gap['matched']) or 'None'}
- Skills missing: {', '.join(skill_gap['missing']) or 'None'}
- Additional skills: {', '.join(skill_gap['extra'][:5]) or 'None'}

Respond in this exact JSON format:
{{
  "recommendation": "STRONG FIT | GOOD FIT | PARTIAL FIT | NOT FIT",
  "hire_reason": "2-3 sentence justification citing specific skills/experience",
  "concern": "1-2 key gaps or risks",
  "suggested_interview_questions": ["Q1", "Q2", "Q3"]
}}"""
