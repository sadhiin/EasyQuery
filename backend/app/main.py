from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.v1.routes import api_router
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="EasyQuery API", version="1.0.0")

# Allow CORS for frontend communication
origins = [
    "http://localhost",
    "http://localhost:8080",
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
