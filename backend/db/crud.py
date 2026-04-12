"""
CRUD operations for database.
Supports both SQLite (local) and Supabase (production).
"""
import uuid
import json
import logging
from typing import Optional, List

logger = logging.getLogger(__name__)


def create_lesson(title: str, category: str, content: dict) -> str:
    """
    Create a new lesson in the database.
    
    Args:
        title: Lesson title
        category: Learner category
        content: Generated content dictionary
    
    Returns:
        Lesson ID
    """
    lesson_id = str(uuid.uuid4())[:8]
    
    try:
        from db.database import db_manager
        db_manager.create_lesson(lesson_id, title, category, content)
        logger.info(f"Created lesson: {lesson_id}")
        return lesson_id
    except Exception as e:
        logger.error(f"Failed to create lesson: {e}")
        raise


def get_lesson(lesson_id: str) -> Optional[dict]:
    """
    Get a lesson by ID.
    
    Args:
        lesson_id: Lesson ID
    
    Returns:
        Lesson data or None
    """
    try:
        from db.database import db_manager
        return db_manager.get_lesson(lesson_id)
    except Exception as e:
        logger.error(f"Failed to get lesson {lesson_id}: {e}")
        return None


def get_all_lessons(skip: int = 0, limit: int = 100) -> List[dict]:
    """
    Get all lessons with pagination.
    
    Args:
        skip: Number of lessons to skip
        limit: Maximum lessons to return
    
    Returns:
        List of lessons
    """
    try:
        from db.database import db_manager
        return db_manager.get_all_lessons(skip, limit)
    except Exception as e:
        logger.error(f"Failed to get lessons: {e}")
        return []
