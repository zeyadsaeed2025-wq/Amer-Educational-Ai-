from fastapi import APIRouter, HTTPException
from db.schemas import ContentRequest, ContentResponse
from db.crud import create_lesson
from core.ai_service import ai_service

router = APIRouter()


@router.post("/api/generate-content", response_model=ContentResponse)
async def generate_content(request: ContentRequest):
    """
    Generate educational content for a given title and learner category.
    
    Returns three versions:
    - standard: Regular educational content
    - simplified: Easy-to-read version
    - accessibility: Accessible version for special needs
    """
    try:
        # Generate content using AI service
        content = await ai_service.generate_content(request.title, request.category)
        
        # Save to database
        category_value = request.category.value if hasattr(request.category, 'value') else request.category
        lesson_id = create_lesson(request.title, category_value, content)
        
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
        raise HTTPException(status_code=500, detail=f"Failed to generate content: {str(e)}")
