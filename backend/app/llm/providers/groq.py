from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from typing import Dict, Any

from ..base import BaseLLMEngine
from ...core.config import settings


class GroqEngine(BaseLLMEngine):
    def __init__(self, model_name: str = "", api_key=settings.GROQ_API_KEY):
        self.llm = ChatGroq(model=model_name, api_key=api_key)

    async def generate_sql(
        self, natural_language_query: str, db_schema: Dict[str, Any]
    ) -> str:
        prompt = self._create_prompt(natural_language_query, db_schema)
        response = self.llm.invoke(prompt)
        return response["messages"][0].content

    def _create_prompt(self, query: str, schema: Dict[str, Any]) -> str:
        template = """
        Based on the table schema below, write a SQL query that would answer the user's question.
        Schema: {schema}
        
        Question: {query}
        
        SQL Query:
        """
        prompt_template = ChatPromptTemplate.from_template(template)
        return prompt_template.format(schema=schema, query=query)
