import uuid
import json
import logging
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from db.schemas import ContentRequest, ContentResponse
from core.ai_service import ai_service

logger = logging.getLogger(__name__)
router = APIRouter()


class GenerateRequest(BaseModel):
    title: str
    category: str = "standard"
    save_to_db: bool = True


class VersionRequest(BaseModel):
    lesson_id: str
    content_standard: str
    content_simplified: str
    content_accessibility: str
    change_summary: str = ""


_supabase_client = None


def get_supabase():
    global _supabase_client
    if _supabase_client is None:
        from core.config import get_settings
        settings = get_settings()
        if settings.supabase_url and settings.supabase_key:
            try:
                from supabase import create_client
                _supabase_client = create_client(settings.supabase_url, settings.supabase_key)
            except Exception as e:
                logger.warning(f"Supabase init failed: {e}")
    return _supabase_client


def save_lesson(title: str, category: str, content: dict, user_id: Optional[str] = None) -> Optional[str]:
    """Save lesson to Supabase with versioning."""
    supabase = get_supabase()
    if not supabase:
        return None
    
    try:
        lesson_id = str(uuid.uuid4())[:8]
        lesson_data = {
            "id": lesson_id,
            "user_id": user_id,
            "title": title,
            "category": category,
            "version": 1,
            "content_standard": json.dumps(content["standard"], ensure_ascii=False),
            "content_simplified": json.dumps(content["simplified"], ensure_ascii=False),
            "content_accessibility": json.dumps(content["accessibility"], ensure_ascii=False),
            "ui_hints": json.dumps(content["ui_hints"], ensure_ascii=False),
        }
        supabase.table("lessons").insert(lesson_data).execute()
        
        version_data = {
            "lesson_id": lesson_id,
            "version": 1,
            "content_standard": json.dumps(content["standard"], ensure_ascii=False),
            "content_simplified": json.dumps(content["simplified"], ensure_ascii=False),
            "content_accessibility": json.dumps(content["accessibility"], ensure_ascii=False),
            "change_summary": "Initial version",
        }
        supabase.table("lesson_versions").insert(version_data).execute()
        
        logger.info(f"Saved lesson {lesson_id} to Supabase")
        return lesson_id
    except Exception as e:
        logger.warning(f"Failed to save lesson: {e}")
        return None


@router.post("/api/generate-content", response_model=ContentResponse)
async def generate_content(
    request: ContentRequest,
    authorization: Optional[str] = Header(None)
):
    """
    Generate educational content with AI.
    Saves to database if authenticated.
    """
    try:
        content = await ai_service.generate_content(request.title, request.category)
        
        category_value = request.category.value if hasattr(request.category, 'value') else request.category
        
        user_id = None
        if authorization and authorization.startswith("Bearer "):
            token = authorization[7:]
            supabase = get_supabase()
            if supabase:
                try:
                    user = supabase.auth.get_user(token)
                    user_id = user.user.id
                except:
                    pass
        
        lesson_id = None
        if user_id or True:
            lesson_id = save_lesson(request.title, category_value, content, user_id)
        
        if not lesson_id:
            lesson_id = str(uuid.uuid4())[:8]
        
        return ContentResponse(
            id=lesson_id,
            title=request.title,
            category=category_value,
            standard=content["standard"],
            simplified=content["simplified"],
            accessibility=content["accessibility"],
            ui_hints=content["ui_hints"],
        )
    except Exception as e:
        logger.error(f"Generate error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate: {str(e)}")


@router.post("/api/lessons/{lesson_id}/versions")
async def create_version(
    lesson_id: str,
    request: VersionRequest,
    authorization: Optional[str] = Header(None)
):
    """Save a new version of a lesson."""
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        current = supabase.table("lessons").select("version").eq("id", lesson_id).execute()
        new_version = (current.data[0]["version"] + 1) if current.data else 1
        
        supabase.table("lessons").update({
            "version": new_version,
            "content_standard": request.content_standard,
            "content_simplified": request.content_simplified,
            "content_accessibility": request.content_accessibility,
            "updated_at": datetime.now().isoformat(),
        }).eq("id", lesson_id).execute()
        
        supabase.table("lesson_versions").insert({
            "lesson_id": lesson_id,
            "version": new_version,
            "content_standard": request.content_standard,
            "content_simplified": request.content_simplified,
            "content_accessibility": request.content_accessibility,
            "change_summary": request.change_summary,
        }).execute()
        
        return {"success": True, "version": new_version}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/lessons/my")
async def get_my_lessons(authorization: Optional[str] = Header(None)):
    """Get user's lesson history."""
    supabase = get_supabase()
    if not supabase:
        return {"lessons": []}
    
    if not authorization or not authorization.startswith("Bearer "):
        return {"lessons": []}
    
    try:
        token = authorization[7:]
        user = supabase.auth.get_user(token)
        user_id = user.user.id
        
        lessons = supabase.table("lessons").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(50).execute()
        return {"lessons": lessons.data}
    except Exception as e:
        logger.warning(f"Failed to get lessons: {e}")
        return {"lessons": []}


@router.get("/api/lessons/{lesson_id}/history")
async def get_lesson_history(lesson_id: str):
    """Get version history for a lesson."""
    supabase = get_supabase()
    if not supabase:
        return {"versions": []}
    
    try:
        versions = supabase.table("lesson_versions").select("*").eq("lesson_id", lesson_id).order("version", desc=True).execute()
        return {"versions": versions.data}
    except Exception as e:
        return {"versions": []}