from app.llm.base import BaseLLMEngine
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from typing import Dict, Any

class GeminiEngine(BaseLLMEngine):
    def __init__(self, model_name: str = "", api_key: str = ""):
        self.llm = ChatGoogleGenerativeAI(google_api_key=api_key, model=model_name, temperature=0)

    async def generate_sql(self, natural_language_query: str, db_schema: Dict[str, Any]) -> str:
        prompt = self._create_prompt(natural_language_query, db_schema)
        response = self.llm.invoke(prompt)
        return response.content

    def _create_prompt(self, query: str, schema: Dict[str, Any]) -> str:
        template = """
        Based on the table schema below, write a SQL query that would answer the user's question.
        Schema: {schema}
        
        Question: {query}
        
        SQL Query:
        """
        prompt_template = ChatPromptTemplate.from_template(template)
        return prompt_template.format(schema=schema, query=query)