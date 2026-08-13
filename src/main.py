from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.upload import router as upload_router
from src.api.chat import router as chat_router
from src.api.voice import router as voice_router
from src.api.videos import router as videos_router

app = FastAPI(
    title="AI Video Q&A Assistant"
)

import os

# Get allowed origins from environment variable, fallback to localhost for development
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(voice_router)
app.include_router(videos_router)


@app.get("/")
async def home():
    return {
        "message": "Welcome to AI Video Q&A Assistant"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }