import os
from endee import Endee
from dotenv import load_dotenv

load_dotenv()
client = Endee(token=os.getenv("ENDEE_TOKEN"))
client.set_base_url(os.getenv("ENDEE_URL"))

def find_matching_resumes(jd_vector: list, top_k: int = 10,
                           min_exp: int = 0, required_skills: list = None):
    """
    Semantic search with metadata filtering — shows Endee's filtering power
    """
    filters = {}
    if min_exp > 0:
        filters["years_exp"] = {"$gte": min_exp}

    results = client.search(
        index_name="resumes",
        query_vector=jd_vector,
        top_k=top_k,
        filters=filters if filters else None,
        include_metadata=True
    )
    return results
