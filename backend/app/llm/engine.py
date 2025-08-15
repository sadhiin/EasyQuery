from app.llm.base import BaseLLMEngine
from app.llm.providers.openai import OpenAIEngine
from app.llm.providers.gemini import GeminiEngine
from app.llm.providers.anthropic import AnthropicEngine
from app.llm.providers.groq import GroqEngine
from app.core.config import settings

def get_llm_engine(provider: str) -> BaseLLMEngine:
    if provider == "openai":
        return OpenAIEngine(model_name=settings.OPENAI_MODEL_NAME, api_key=settings.OPENAI_API_KEY)
    elif provider == "gemini":
        return GeminiEngine(model_name=settings.GEMINI_MODEL_NAME, api_key=settings.GEMINI_API_KEY)
    elif provider == "anthropic":
        return AnthropicEngine(model_name=settings.ANTHROPIC_MODEL_NAME, api_key=settings.ANTHROPIC_API_KEY)
    elif provider == "groq":
        return GroqEngine(model_name=settings.GROQ_MODEL_NAME, api_key=settings.GROQ_API_KEY)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")