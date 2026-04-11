def compute_skill_gap(required_skills: list, candidate_skills: list) -> dict:
    required = set(s.lower() for s in required_skills)
    present  = set(s.lower() for s in candidate_skills)
    matched  = required & present
    missing  = required - present
    extra    = present - required

    match_pct = round(len(matched) / len(required) * 100) if required else 0
    return {
        "match_pct": match_pct,
        "matched": list(matched),
        "missing": list(missing),
        "extra": list(extra),
        "score": match_pct / 100
    }

def combined_score(semantic_score: float, skill_gap_score: float,
                   exp_score: float) -> float:
    """Weighted composite — tunable"""
    return round(
        0.50 * semantic_score +
        0.35 * skill_gap_score +
        0.15 * exp_score, 3
    )
