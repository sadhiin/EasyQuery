from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException as FastAPIHTTPException
from starlette.middleware.cors import CORSMiddleware
from app.api.v1.routes import api_router
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="EasyQuery API", version="1.0.0")

# Allow CORS for frontend communication
origins = [
    "*",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to EasyQuery Backend!"}


@app.exception_handler(FastAPIHTTPException)
async def http_exception_handler(request: Request, exc: FastAPIHTTPException):
    # Ensure HTTPExceptions return JSON with a consistent shape
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log full traceback server-side and return a safe JSON error to the client
    logger.exception(f"Unhandled error: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
