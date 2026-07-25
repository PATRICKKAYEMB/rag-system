import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    # Remplace "models/text-embedding-004" par "text-embedding-004"
    
    EMBEDDING_MODEL: str = "models/gemini-embedding-001"

    LLM_MODEL: str = "gemini-2.5-flash"

settings = Settings()