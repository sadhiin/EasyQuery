from sqlalchemy import create_engine, text, inspect, Engine
from fastapi import HTTPException
from typing import Optional
import logging
from decimal import Decimal
import json
from datetime import datetime, date, time

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.engine: Optional[Engine] = None

    def _sanitize_db_url(self, db_url: str) -> str:
        """
        Remove problematic SSL parameters that may cause connection issues in Docker environments.
        Specifically handles channel_binding parameter which may not be supported by all PostgreSQL servers.
        """
        try:
            # Simple string replacement approach to avoid URL parsing complications
            if 'channel_binding=require' in db_url:
                logger.info("Removing channel_binding=require parameter from database URL for compatibility")
                # Remove the parameter and any preceding & or ?
                sanitized_url = db_url.replace('&channel_binding=require', '')
                sanitized_url = sanitized_url.replace('?channel_binding=require&', '?')
                sanitized_url = sanitized_url.replace('?channel_binding=require', '')
                return sanitized_url
            elif 'channel_binding=' in db_url:
                logger.info("Removing channel_binding parameter from database URL for compatibility")
                # Handle any channel_binding value
                import re
                sanitized_url = re.sub(r'[&?]channel_binding=[^&]*', '', db_url)
                # Clean up any double & or trailing & or ?
                sanitized_url = re.sub(r'[&]{2,}', '&', sanitized_url)
                sanitized_url = re.sub(r'[?&]$', '', sanitized_url)
                sanitized_url = re.sub(r'\?&', '?', sanitized_url)
                return sanitized_url
            return db_url
        except Exception as e:
            logger.warning(f"Failed to sanitize database URL: {e}. Using original URL.")
            return db_url

    async def connect(self):
        try:
            # First, try with the original URL
            self.engine = create_engine(self.db_url)
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            logger.info(f"Successfully connected to database: {self.db_url}")
            return True
        except Exception as e:
            logger.warning(f"Initial connection failed: {e}")
            
            # If the error is related to channel binding, try with sanitized URL
            if "channel binding" in str(e).lower() or "channel_binding" in str(e).lower():
                try:
                    sanitized_url = self._sanitize_db_url(self.db_url)
                    logger.info("Retrying connection with sanitized URL (removed channel_binding)")
                    
                    # Dispose of the previous engine if it exists
                    if self.engine:
                        self.engine.dispose()
                    
                    self.engine = create_engine(sanitized_url)
                    with self.engine.connect() as connection:
                        connection.execute(text("SELECT 1"))
                    logger.info(f"Successfully connected to database with sanitized URL")
                    return True
                except Exception as retry_e:
                    logger.error(f"Failed to connect with sanitized URL: {retry_e}")
                    raise HTTPException(status_code=400, detail=f"Database connection failed: {retry_e}")
            else:
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
                    rows = []
                    for row in result.mappings():
                        row_dict = {}
                        for key, value in row.items():
                            # Convert Decimal to float for JSON serialization
                            if isinstance(value, Decimal):
                                row_dict[key] = float(value)
                            # Convert datetime objects to ISO format strings
                            elif isinstance(value, (datetime, date, time)):
                                if isinstance(value, datetime):
                                    row_dict[key] = value.isoformat()
                                elif isinstance(value, date):
                                    row_dict[key] = value.isoformat()
                                elif isinstance(value, time):
                                    row_dict[key] = value.isoformat()
                            else:
                                row_dict[key] = value
                        rows.append(row_dict)
                    # rows = CustomJSONResponse.render(result.mappings())
                    return rows
                return {"message": "Query executed successfully, no rows returned."}
        except Exception as e:
            logger.error(f"Failed to execute query '{query}' on {self.db_url}: {e}")
            raise HTTPException(status_code=400, detail=f"Query execution failed: {e}")