import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def get_secret_or_env(key: str, default: str = "") -> str:
    val = os.getenv(key)
    if val:
        return val
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass
    return default

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = DATA_DIR / "chroma_db"
DOWNLOADS_DIR = DATA_DIR / "downloads"
SQLITE_DB_PATH = DATA_DIR / "paperpulse.db"
EVAL_RESULTS_PATH = DATA_DIR / "eval_results.json"

DATA_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DIR.mkdir(parents=True, exist_ok=True)
DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)

# Default LLM & Embedding Settings
DEFAULT_EMBEDDING_MODEL = get_secret_or_env("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
DEFAULT_LLM_PROVIDER = get_secret_or_env("LLM_PROVIDER", "gemini")
DEFAULT_LLM_MODEL = get_secret_or_env("LLM_MODEL", "gemini-2.5-flash")

# API Keys (Optional with offline fallback)
GEMINI_API_KEY = get_secret_or_env("GEMINI_API_KEY") or get_secret_or_env("GOOGLE_API_KEY", "")
OPENAI_API_KEY = get_secret_or_env("OPENAI_API_KEY", "")
GROQ_API_KEY = get_secret_or_env("GROQ_API_KEY", "")

# ArXiv Sourcing Defaults
DEFAULT_ARXIV_CATEGORIES = [
    {"code": "cs.AI", "name": "Artificial Intelligence", "desc": "Frontier architectures, agents & reasoning"},
    {"code": "cs.LG", "name": "Machine Learning", "desc": "Deep learning, optimization & theory"},
    {"code": "cs.CL", "name": "Computation & Language", "desc": "LLMs, NLP & Multimodal Foundation Models"},
    {"code": "cs.CV", "name": "Computer Vision", "desc": "Vision Transformers, Diffusion & Generative Models"},
    {"code": "stat.ML", "name": "Stat Machine Learning", "desc": "Probabilistic models & statistical guarantees"}
]

# Retrieval & Chunking Settings
SECTION_CHUNK_SIZE = int(get_secret_or_env("SECTION_CHUNK_SIZE", "500"))
SECTION_CHUNK_OVERLAP = int(get_secret_or_env("SECTION_CHUNK_OVERLAP", "75"))
TOP_K_PAPERS = int(get_secret_or_env("TOP_K_PAPERS", "5"))
CITATION_GRAPH_MAX_HOPS = int(get_secret_or_env("CITATION_GRAPH_MAX_HOPS", "2"))
INFLUENTIAL_CITATION_LIMIT = int(get_secret_or_env("INFLUENTIAL_CITATION_LIMIT", "5"))
SIMILARITY_THRESHOLD = float(get_secret_or_env("SIMILARITY_THRESHOLD", "0.35"))
