from app.llm.base import BaseLLMEngine
from app.llm.providers.openai import OpenAIEngine
from app.llm.providers.gemini import GeminiEngine
from app.llm.providers.anthropic import AnthropicEngine
from app.llm.providers.groq import GroqEngine
from app.core.config import settings

def get_llm_engine(provider: str) -> BaseLLMEngine:
    if provider == "openai":
        return OpenAIEngine(api_key=settings.OPENAI_API_KEY)
    elif provider == "gemini":
        return GeminiEngine(api_key=settings.GEMINI_API_KEY)
    elif provider == "anthropic":
        return AnthropicEngine(api_key=settings.ANTHROPIC_API_KEY)
    elif provider == "groq":
        return GroqEngine(api_key=settings.GROQ_API_KEY)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")