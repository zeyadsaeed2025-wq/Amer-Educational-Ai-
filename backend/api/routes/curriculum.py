import uuid
import json
import logging
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.ai_service import ai_service

logger = logging.getLogger(__name__)
router = APIRouter()

# Curriculum schemas
class CurriculumRequest(BaseModel):
    title: str
    category: str = "standard"
    num_units: int = 3
    lessons_per_unit: int = 4


class LessonOutline(BaseModel):
    title: str
    objectives: list = []
    duration_minutes: int = 30


class UnitOutline(BaseModel):
    unit_title: str
    lessons: list = []
    assessment: str = ""


class CurriculumResponse(BaseModel):
    course_id: str
    course_title: str
    category: str
    objectives: list
    units: list
    total_lessons: int
    estimated_hours: int


class LiveAssistRequest(BaseModel):
    text: str
    context: str = "general"
    category: str = "standard"


class LiveAssistResponse(BaseModel):
    suggestions: list
    improved_text: str
    improvements: list


class SmartAnalyzeRequest(BaseModel):
    text: str
    category: str = "standard"


class SmartAnalyzeResponse(BaseModel):
    score: int
    engagement_level: str
    complexity_level: str
    alerts: list
    suggestions: list
    readability_score: int
    interactivity_score: int


@router.post("/api/curriculum/generate", response_model=CurriculumResponse)
async def generate_curriculum(request: CurriculumRequest):
    """
    Generate a complete curriculum with units and lessons.
    """
    try:
        curriculum = await ai_service.generate_curriculum(
            request.title,
            request.category,
            request.num_units,
            request.lessons_per_unit
        )
        
        course_id = str(uuid.uuid4())[:8]
        
        return CurriculumResponse(
            course_id=course_id,
            course_title=curriculum.get("course_title", request.title),
            category=request.category,
            objectives=curriculum.get("objectives", []),
            units=curriculum.get("units", []),
            total_lessons=curriculum.get("total_lessons", 0),
            estimated_hours=curriculum.get("estimated_hours", 0),
        )
    except Exception as e:
        logger.error(f"Curriculum generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/live-assist", response_model=LiveAssistResponse)
async def live_assist(request: LiveAssistRequest):
    """
    Get AI assistance while editing content.
    """
    try:
        result = await ai_service.live_assist(
            request.text,
            request.context,
            request.category
        )
        
        return LiveAssistResponse(
            suggestions=result.get("suggestions", []),
            improved_text=result.get("improved_text", ""),
            improvements=result.get("improvements", []),
        )
    except Exception as e:
        logger.error(f"Live assist error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/smart-analyze", response_model=SmartAnalyzeResponse)
async def smart_analyze(request: SmartAnalyzeRequest):
    """
    AI-powered content analysis with smart alerts.
    """
    try:
        result = await ai_service.smart_analyze(
            request.text,
            request.category
        )
        
        return SmartAnalyzeResponse(
            score=result.get("score", 0),
            engagement_level=result.get("engagement_level", "medium"),
            complexity_level=result.get("complexity_level", "medium"),
            alerts=result.get("alerts", []),
            suggestions=result.get("suggestions", []),
            readability_score=result.get("readability_score", 0),
            interactivity_score=result.get("interactivity_score", 0),
        )
    except Exception as e:
        logger.error(f"Smart analyze error: {e}")
        raise HTTPException(status_code=500, detail=str(e))