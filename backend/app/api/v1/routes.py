from fastapi import APIRouter
from .endpoints import connection_router, query_router

api_router = APIRouter()
api_router.include_router(connection_router, prefix="/connection", tags=["connection"])
api_router.include_router(query_router, prefix="/query", tags=["query"])