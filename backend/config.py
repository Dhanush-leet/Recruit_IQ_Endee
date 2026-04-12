import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY  = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.together.xyz/v1")
EMBED_MODEL     = os.getenv("EMBED_MODEL", "intfloat/multilingual-e5-large-instruct")
EMBED_DIM       = int(os.getenv("EMBED_DIM", "1024"))
LLM_MODEL       = os.getenv("LLM_MODEL", "meta-llama/Llama-3.3-70B-Instruct-Turbo")

ENDEE_URL       = os.getenv("ENDEE_URL", "http://localhost:8080/api/v1")
ENDEE_TOKEN     = os.getenv("ENDEE_TOKEN", "")
INDEX_NAME      = os.getenv("INDEX_NAME", "recruitiq_resumes")
JD_INDEX_NAME   = os.getenv("JD_INDEX_NAME", "recruitiq_jds")

BATCH_SIZE      = int(os.getenv("BATCH_SIZE", "50"))
TOP_K           = int(os.getenv("TOP_K", "8"))
MAX_CHUNK_CHARS = int(os.getenv("MAX_CHUNK_CHARS", "1500"))
