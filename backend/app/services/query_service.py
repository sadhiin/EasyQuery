import speech_recognition as sr
import tempfile
import os
import logging
from fastapi import HTTPException, UploadFile
from app.api.v1.db import DatabaseManager
from app.llm.engine import get_llm_engine

logger = logging.getLogger(__name__)

# In-memory store for database connections.
db_connections: dict[str, DatabaseManager] = {}

async def process_text_query(session_id: str, query_text: str, llm_provider: str):
    db_manager = db_connections.get(session_id)
    if not db_manager:
        raise HTTPException(status_code=400, detail="No database connected for this session.")

    llm_engine = get_llm_engine(llm_provider)
    db_schema = await db_manager.fetch_schema()
    generated_sql_query = await llm_engine.generate_sql(query_text, db_schema)
    
    try:
        result = await db_manager.execute_query(generated_sql_query)
        return {"message": "Query executed", "results": result, "sql_query": generated_sql_query}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error during query: {e}")

async def process_speech_query_service(session_id: str, audio_file: UploadFile, llm_provider: str):
    db_manager = db_connections.get(session_id)
    if not db_manager:
        raise HTTPException(status_code=400, detail="No database connected for this session.")

    r = sr.Recognizer()
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(await audio_file.read())
            temp_audio_path = temp_audio.name
        
        with sr.AudioFile(temp_audio_path) as source:
            audio_data = r.record(source)
        
        os.remove(temp_audio_path)

        text_query = r.recognize_google(audio_data)
        logger.info(f"Speech-to-text converted: {text_query}")

        llm_engine = get_llm_engine(llm_provider)
        db_schema = await db_manager.fetch_schema()
        generated_sql_query = await llm_engine.generate_sql(text_query, db_schema)

        result = await db_manager.execute_query(generated_sql_query)
        return {"message": "Speech query processed", "text_query": text_query, "results": result, "sql_query": generated_sql_query}

    except sr.UnknownValueError:
        raise HTTPException(status_code=400, detail="Could not understand audio")
    except sr.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Speech service error: {e}")
    except Exception as e:
        logger.error(f"Error processing speech query: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error processing speech: {e}")

async def get_schema(session_id: str):
    db_manager = db_connections.get(session_id)
    if not db_manager:
        raise HTTPException(status_code=400, detail="No database connected for this session.")
    try:
        schema = await db_manager.fetch_schema()
        return {"schema": schema}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error fetching schema: {e}")