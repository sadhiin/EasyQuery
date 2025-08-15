from typing import Literal
from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import JSONResponse
from app.models.pydantic_models import QueryRequest
from app.services.query_service import process_text_query, process_speech_query_service, get_schema

query_router = APIRouter()


@query_router.post("/query")
async def process_query(request: QueryRequest):
    session_id = "default_session"
    result = await process_text_query(session_id, request.query_text, request.llm_provider)
    return JSONResponse(status_code=200, content=result)


@query_router.post("/speech-query")
async def process_speech_query(
    audio_file: UploadFile = File(...),
    llm_provider: Literal["openai", "gemini", "anthropic", "groq"] = Form(...)
):
    session_id = "default_session"
    result = await process_speech_query_service(session_id, audio_file, llm_provider)
    return JSONResponse(status_code=200, content=result)


@query_router.get("/schema")
async def get_database_schema():
    session_id = "default_session"
    result = await get_schema(session_id)
    return JSONResponse(status_code=200, content=result)