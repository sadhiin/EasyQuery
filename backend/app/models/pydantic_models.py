from pydantic import BaseModel
from typing import Literal


class ConnectRequest(BaseModel):
    db_url: str


class QueryRequest(BaseModel):
    query_text: str
    llm_provider: Literal["openai", "gemini", "anthropic", "groq"]
