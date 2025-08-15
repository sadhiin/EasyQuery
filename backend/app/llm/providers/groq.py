from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from typing import Dict, Any

from ..base import BaseLLMEngine
from ...core.config import settings
from ...utils.clean_code import clean_ai_response

class GroqEngine(BaseLLMEngine):
    def __init__(self, model_name: str = "", api_key=settings.GROQ_API_KEY):
        self.llm = ChatGroq(model=model_name, api_key=api_key, temperature=0)

    async def generate_sql(
        self, natural_language_query: str, db_schema: Dict[str, Any]
    ) -> str:
        prompt = self._create_prompt(natural_language_query, db_schema)
        response = self.llm.invoke(prompt)
        return clean_ai_response(response.content)

    def _create_prompt(self, query: str, schema: Dict[str, Any]) -> str:
        template = """
        Based on the table schema below, write a SQL query that would answer the user's question. **No need to give any other text other then sql query, because right after that this query will give to sql engine to execute**
        This SQL will be executed against the following schema:
        Schema: {schema}
        
        Question: {query}
        
        SQL Query:
        """
        prompt_template = ChatPromptTemplate.from_template(template)
        return prompt_template.format(schema=schema, query=query)
