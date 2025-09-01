import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    # llm models
    OPENAI_MODEL_NAME: str = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
    GEMINI_MODEL_NAME: str = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash")
    ANTHROPIC_MODEL_NAME: str = os.getenv("ANTHROPIC_MODEL_NAME", "claude-3-5-haiku-20241022")
    GROQ_MODEL_NAME: str = os.getenv("GROQ_MODEL_NAME", "openai/gpt-oss-20b")

    # sql configs
    SQLALCHEMY_DATABASE_URL: str = os.getenv("SQLALCHEMY_DATABASE_URL", "sqlite:///./test.db")

settings = Settings()
