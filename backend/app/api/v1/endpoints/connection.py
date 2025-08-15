from fastapi import APIRouter, HTTPException
from app.models.pydantic_models import ConnectRequest
from ..db import DatabaseManager
from app.services.query_service import db_connections

connection_router = APIRouter()

@connection_router.post("/connect")
async def connect_to_database(request: ConnectRequest):
    session_id = "default_session"  # In a real app, use a unique session ID per user
    db_manager = DatabaseManager(request.db_url)
    try:
        await db_manager.connect()
        db_connections[session_id] = db_manager
        return {"message": "Database connected successfully!", "db_url": request.db_url}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error during connection: {e}")