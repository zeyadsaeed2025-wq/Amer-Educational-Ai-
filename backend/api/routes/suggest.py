from fastapi import APIRouter, HTTPException
from db.schemas import SuggestionRequest, SuggestionResponse
from core.ai_service import ai_service

router = APIRouter()


@router.post("/api/suggest-improvements", response_model=SuggestionResponse)
async def suggest_improvements(request: SuggestionRequest) -> SuggestionResponse:
    """
    Generate AI-powered improvement suggestions for content.
    """
    try:
        suggestions = await ai_service.generate_improvements(request.text)
        return SuggestionResponse(suggestions=suggestions)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"فشل توليد الاقتراحات: {str(e)}")
