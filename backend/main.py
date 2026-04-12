import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.database import db_manager
from db.schemas import HealthResponse
from core.config import get_settings
from api.routes.generate import router as generate_router
from api.routes.analyze import router as analyze_router
from api.routes.suggest import router as suggest_router
from api.routes.lessons import router as lessons_router
from api.websocket import websocket_endpoint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown."""
    logger.info(f"Starting {settings.app_name}...")
    logger.info(f"Database: {'Supabase' if db_manager._supabase else 'SQLite'}")
    yield
    logger.info("Shutting down...")


app = FastAPI(
    title=settings.app_name,
    description="AI-powered educational content generation API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS Middleware
origins = settings.cors_origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(generate_router)
app.include_router(analyze_router)
app.include_router(suggest_router)
app.include_router(lessons_router)


@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint."""
    return HealthResponse(
        status="ok",
        service=settings.app_name,
        version="1.0.0",
        timestamp=datetime.now().isoformat(),
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check."""
    return HealthResponse(
        status="healthy",
        service=settings.app_name,
        version="1.0.0",
        timestamp=datetime.now().isoformat(),
    )


@app.websocket("/ws")
async def ws_endpoint(websocket):
    """WebSocket endpoint for real-time analysis."""
    await websocket_endpoint(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
