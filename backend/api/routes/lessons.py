from fastapi import APIRouter, HTTPException, Query
from typing import List
from db.crud import get_lesson, get_all_lessons

router = APIRouter()


@router.get("/api/lessons")
async def list_lessons(
    skip: int = Query(0, ge=0, description="Number of lessons to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum lessons to return"),
):
    """
    Get all lessons with pagination.
    
    - skip: Number of lessons to skip (for pagination)
    - limit: Maximum number of lessons to return (default 10, max 100)
    """
    try:
        lessons = get_all_lessons(skip=skip, limit=limit)
        return {
            "lessons": lessons,
            "total": len(lessons),
            "skip": skip,
            "limit": limit,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/lessons/{lesson_id}")
async def get_lesson_by_id(lesson_id: str):
    """
    Get a specific lesson by ID.
    """
    try:
        lesson = get_lesson(lesson_id)
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")
        return lesson
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
