import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from db.schemas import HealthResponse
from core.config import get_settings
from api.routes.generate import router as generate_router
from api.routes.analyze import router as analyze_router
from api.routes.suggest import router as suggest_router
from api.routes.lessons import router as lessons_router
from api.routes.curriculum import router as curriculum_router
from api.websocket import websocket_endpoint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_type = "PostgreSQL" if os.getenv("DATABASE_URL") else ("Supabase" if os.getenv("SUPABASE_URL") else "SQLite")
    cache_type = "Redis" if os.getenv("REDIS_URL") else "None"
    logger.info(f"Starting {settings.app_name}...")
    logger.info(f"Database: {db_type}")
    logger.info(f"Cache: {cache_type}")
    yield
    logger.info("Shutting down...")


app = FastAPI(
    title=settings.app_name,
    description="AI-powered educational content generation API",
    version="1.0.0",
    lifespan=lifespan,
)


# Root - serve frontend or health info
@app.get("/")
async def root():
    """Serve frontend HTML or API info."""
    try:
        return FileResponse("index.html", media_type="text/html")
    except:
        return {"status": "ok", "service": "EduForge AI", "version": "1.0.0"}


# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        service=settings.app_name,
        version="1.0.0",
        timestamp=datetime.now().isoformat(),
    )


# CORS - Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(generate_router)
app.include_router(analyze_router)
app.include_router(suggest_router)
app.include_router(lessons_router)
app.include_router(curriculum_router)


# WebSocket for real-time (local only)
@app.websocket("/ws")
async def ws_endpoint(websocket):
    await websocket_endpoint(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=settings.debug)
