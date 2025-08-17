import speech_recognition as sr
import tempfile
import os
import logging
from fastapi import HTTPException, UploadFile
from app.api.v1.db import DatabaseManager
from app.llm.engine import get_llm_engine
from pydub import AudioSegment

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
        # Get the file extension from the content type
        content_type = audio_file.content_type or "audio/webm"
        file_extension = content_type.split('/')[-1]
        
        # Create a temporary file with the appropriate extension
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_audio:
            temp_audio.write(await audio_file.read())
            temp_audio_path = temp_audio.name
        
        # Convert to WAV format if needed
        wav_path = None
        try:
            if file_extension.lower() != 'wav':
                # Convert to WAV using pydub
                audio = AudioSegment.from_file(temp_audio_path, format=file_extension)
                wav_path = temp_audio_path.replace(f".{file_extension}", ".wav")
                audio.export(wav_path, format="wav")
                audio_file_path = wav_path
            else:
                audio_file_path = temp_audio_path
            
            # Use the audio file for speech recognition
            with sr.AudioFile(audio_file_path) as source:
                audio_data = r.record(source)
        
        except Exception as conversion_error:
            logger.error(f"Audio conversion failed: {conversion_error}")
            raise HTTPException(status_code=500, detail=f"Audio format conversion failed: {content_type}")
        
        finally:
            # Clean up temporary files
            os.remove(temp_audio_path)
            if wav_path:
                os.remove(wav_path)

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

async def speech_to_text_only(session_id: str, audio_file: UploadFile):
    """
    Convert speech to text without executing any query.
    Returns only the converted text.
    """
    r = sr.Recognizer()
    try:
        # Get the file extension from the content type
        content_type = audio_file.content_type or "audio/webm"
        file_extension = content_type.split('/')[-1]
        
        # Create a temporary file with the appropriate extension
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_audio:
            temp_audio.write(await audio_file.read())
            temp_audio_path = temp_audio.name
        
        # Convert to WAV format if needed
        wav_path = None
        try:
            if file_extension.lower() != 'wav':
                # Convert to WAV using pydub
                audio = AudioSegment.from_file(temp_audio_path, format=file_extension)
                wav_path = temp_audio_path.replace(f".{file_extension}", ".wav")
                audio.export(wav_path, format="wav")
                audio_file_path = wav_path
            else:
                audio_file_path = temp_audio_path
            
            # Use the audio file for speech recognition
            with sr.AudioFile(audio_file_path) as source:
                audio_data = r.record(source)
        
        except Exception as conversion_error:
            logger.error(f"Audio conversion failed: {conversion_error}")
            raise HTTPException(status_code=500, detail=f"Audio format conversion failed: {content_type}")
        
        finally:
            # Clean up temporary files
            os.remove(temp_audio_path)
            if wav_path:
                os.remove(wav_path)

        # Try to recognize the speech using Google's service
        try:
            text_query = r.recognize_google(audio_data)
        except sr.RequestError as e:
            logger.error(f"Google speech recognition service error: {e}")
            raise HTTPException(status_code=500, detail="Speech recognition service unavailable")
        
        logger.info(f"Speech-to-text converted: {text_query}")
        
        return {"text_query": text_query}

    except sr.UnknownValueError:
        raise HTTPException(status_code=400, detail="Could not understand audio")
    except sr.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Speech service error: {e}")
    except Exception as e:
        logger.error(f"Error converting speech to text: {e}")
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