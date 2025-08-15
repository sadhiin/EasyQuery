from sqlalchemy import create_engine, text, inspect, Engine
from fastapi import HTTPException
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.engine: Optional[Engine] = None

    async def connect(self):
        try:
            self.engine = create_engine(self.db_url)
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            logger.info(f"Successfully connected to database: {self.db_url}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to database {self.db_url}: {e}")
            raise HTTPException(status_code=400, detail=f"Database connection failed: {e}")

    async def disconnect(self):
        if self.engine:
            self.engine.dispose()
            logger.info(f"Disconnected from database: {self.db_url}")

    async def fetch_schema(self):
        if not self.engine:
            raise HTTPException(status_code=400, detail="Not connected to a database.")

        try:
            with self.engine.connect() as connection:
                inspector = inspect(self.engine)
                tables = inspector.get_table_names()
                schema = {}
                for table_name in tables:
                    columns = [col['name'] for col in inspector.get_columns(table_name)]
                    schema[table_name] = columns
                logger.info(f"Fetched schema for {self.db_url}: {schema}")
                return schema
        except Exception as e:
            logger.error(f"Failed to fetch schema for {self.db_url}: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to fetch schema: {e}")

    async def execute_query(self, query: str):
        if not self.engine:
            raise HTTPException(status_code=400, detail="Not connected to a database.")
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query))
                if result.returns_rows:
                    return [dict(row) for row in result.mappings()]
                return {"message": "Query executed successfully, no rows returned."}
        except Exception as e:
            logger.error(f"Failed to execute query '{query}' on {self.db_url}: {e}")
            raise HTTPException(status_code=400, detail=f"Query execution failed: {e}")