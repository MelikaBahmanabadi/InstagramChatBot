from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "db" / "app_data.sqlite"

LLM_API_URL = os.getenv("LLM_API_URL", "https://apifreellm.com/api/chat")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",") if os.getenv("ALLOWED_ORIGINS") else []
RATE_LIMIT = os.getenv("RATE_LIMIT", "10/minute")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

RAG_TOP_K = 5
MAX_CONTEXT_LENGTH = 2000
