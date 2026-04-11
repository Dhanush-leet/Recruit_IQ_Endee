import os
from endee import Endee, Precision
from dotenv import load_dotenv

load_dotenv()

client = Endee(token=os.getenv("ENDEE_TOKEN"))
client.set_base_url(os.getenv("ENDEE_URL"))

def setup_indexes():
    """Create two indexes: resumes and job_descriptions"""
    existing = [idx['name'] for idx in client.list_indexes()]
    
    if "resumes" not in existing:
        client.create_index(
            name="resumes",
            dimension=384,
            space_type="cosine",
            M=16,
            ef_con=128,
            precision=Precision.INT8D
        )
        print("✅ Created 'resumes' index")

    if "job_descriptions" not in existing:
        client.create_index(
            name="job_descriptions",
            dimension=384,
            space_type="cosine",
            M=16,
            ef_con=128,
            precision=Precision.INT8D
        )
        print("✅ Created 'job_descriptions' index")

def upsert_resume(resume_id: str, vector: list, metadata: dict):
    """
    metadata keys: name, email, skills, years_exp, location, raw_text
    """
    client.upsert(
        index_name="resumes",
        vectors=[{
            "id": resume_id,
            "vector": vector,
            "metadata": metadata
        }]
    )

def upsert_job(job_id: str, vector: list, metadata: dict):
    client.upsert(
        index_name="job_descriptions",
        vectors=[{
            "id": job_id,
            "vector": vector,
            "metadata": metadata
        }]
    )
