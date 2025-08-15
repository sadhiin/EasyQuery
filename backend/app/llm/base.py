from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseLLMEngine(ABC):
    def __init__(self, model_name: str = "", api_key: str = ""):
        pass
    
    @abstractmethod
    async def generate_sql(self, natural_language_query: str, db_schema: Dict[str, Any]) -> str:
        """
        Generates an SQL query from a natural language query and a database schema.
        """
        pass