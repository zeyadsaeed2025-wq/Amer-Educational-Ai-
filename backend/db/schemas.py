from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from core.enums import LearnerCategory, ContentTab


class ContentRequest(BaseModel):
    title: str = Field(..., min_length=2, max_length=200, description="Lesson title")
    category: LearnerCategory = Field(default=LearnerCategory.STANDARD, description="Target learner category")


class ContentVersion(BaseModel):
    intro: str = Field(..., description="Introduction text")
    body: str = Field(..., description="Main body content")
    questions: List[str] = Field(default_factory=list, description="Assessment questions")
    activities: Optional[List[str]] = Field(default=None, description="Learning activities")
    tips: Optional[List[str]] = Field(default=None, description="Learning tips")


class ContentResponse(BaseModel):
    id: str
    title: str
    category: str
    standard: ContentVersion
    simplified: ContentVersion
    accessibility: ContentVersion
    ui_hints: dict = Field(default_factory=dict)
    user_id: Optional[str] = None
    version: int = 1


class AnalysisRequest(BaseModel):
    text: str = Field(..., min_length=10, description="Content to analyze")
    tab: str = Field(default="standard", description="Content version type")


class QualityAlert(BaseModel):
    type: str = Field(..., description="Alert type: warn, danger, or info")
    msg: str = Field(..., description="Alert message")


class QualityMetrics(BaseModel):
    score: int = Field(..., ge=0, le=100)
    readability: int = Field(..., ge=0, le=100)
    interactivity: int = Field(..., ge=0, le=100)
    engagement: int = Field(..., ge=0, le=100)
    alerts: List[QualityAlert] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)


class SuggestionRequest(BaseModel):
    text: str = Field(..., min_length=20, description="Content to analyze")


class SuggestionResponse(BaseModel):
    suggestions: List[str] = Field(default_factory=list)


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    timestamp: Optional[str] = None


# User & Lesson schemas
class UserProfile(BaseModel):
    id: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    created_at: Optional[str] = None


class Lesson(BaseModel):
    id: str
    user_id: Optional[str] = None
    title: str
    category: str
    version: int = 1
    is_published: bool = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class LessonDetail(Lesson):
    content_standard: Optional[str] = None
    content_simplified: Optional[str] = None
    content_accessibility: Optional[str] = None
    ui_hints: Optional[str] = None


class LessonVersion(BaseModel):
    id: str
    lesson_id: str
    version: int
    content_standard: Optional[str] = None
    content_simplified: Optional[str] = None
    content_accessibility: Optional[str] = None
    change_summary: Optional[str] = None
    created_at: Optional[str] = None
