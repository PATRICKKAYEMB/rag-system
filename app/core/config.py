from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME:str ="LangChain FastAPI Agent"
    GOOGLE_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash"


    class Config:
        env_file = ".env"
settings = Settings()