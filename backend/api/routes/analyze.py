from fastapi import APIRouter, HTTPException
from db.schemas import AnalysisRequest, QualityMetrics, QualityAlert
from core.quality_engine import QualityEngine

router = APIRouter()
quality_engine = QualityEngine()


@router.post("/api/analyze-content", response_model=QualityMetrics)
async def analyze_content(request: AnalysisRequest) -> QualityMetrics:
    """
    Analyze content quality and return metrics.
    
    Checks:
    - Readability score
    - Interactivity level
    - Engagement potential
    - Alerts for potential issues
    - Suggestions for improvement
    """
    try:
        metrics = quality_engine.analyze(request.text, request.tab)
        
        return QualityMetrics(
            score=metrics.score,
            readability=metrics.readability,
            interactivity=metrics.interactivity,
            engagement=metrics.engagement,
            alerts=[QualityAlert(type=a.type, msg=a.msg) for a in metrics.alerts],
            suggestions=metrics.suggestions,
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"فشل تحليل المحتوى: {str(e)}")
