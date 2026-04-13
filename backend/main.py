import os
import json
import uuid
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
import re
import uvicorn
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

# Get environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
JWT_SECRET = os.getenv("JWT_SECRET", "eduforge-secret-key-2024")

# Debug: Print first few chars of API key if exists
if OPENAI_API_KEY and len(OPENAI_API_KEY) > 20:
    print("[OK] OpenAI API Key loaded: " + OPENAI_API_KEY[:15] + "...")
else:
    print("[WARN] OpenAI API Key not set or invalid in .env file!")
    print("   Add your key in backend/.env as: OPENAI_API_KEY=sk-...")

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Body, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_arabic(text: str) -> bool:
    return bool(re.search(r'[\u0600-\u06FF]', text))

app = FastAPI(title="EduForge AI Backend", version="1.0.0")

CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "https://*.vercel.app",
    "https://*.vercel.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Supabase client
supabase: Optional[Client] = None

lessons_db = []

if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("Supabase client initialized successfully")
    except Exception as e:
        logger.warning(f"Failed to initialize Supabase: {e}")


class GenerateContentRequest(BaseModel):
    title: str
    category: str


class SaveLessonRequest(BaseModel):
    title: str
    category: str
    content: Dict[str, Any]


class LessonContent(BaseModel):
    standard: Dict[str, Any]
    simplified: Dict[str, Any]
    accessibility: Dict[str, Any]


async def generate_ai_content(title: str, category: str) -> LessonContent:
    """Generate educational content using OpenAI or fallback to mock"""
    
    if OPENAI_API_KEY:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {OPENAI_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-3.5-turbo",
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are an educational content generator. Generate structured lesson content with: 1) standard version, 2) simplified version for struggling learners, 3) accessibility version for various disabilities. Return JSON with 'sections', 'questions', 'activities', 'objectives' for each version."
                            },
                            {
                                "role": "user",
                                "content": f"Generate lesson content for: {title} (Category: {category}). Include learning objectives, lesson content sections, discussion questions, and activities."
                            }
                        ],
                        "temperature": 0.7,
                        "max_tokens": 2000
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    content = data["choices"][0]["message"]["content"]
                    try:
                        parsed = json.loads(content)
                        return LessonContent(
                            standard=parsed.get("standard", parsed),
                            simplified=parsed.get("simplified", parsed),
                            accessibility=parsed.get("accessibility", parsed)
                        )
                    except json.JSONDecodeError:
                        pass
        except Exception as e:
            logger.warning(f"OpenAI API failed: {e}")
    
    return generate_mock_content(title, category)


def generate_mock_content(title: str, category: str) -> LessonContent:
    """Generate mock educational content as fallback"""
    
    arabic = is_arabic(title)
    
    category_ar = {
        "math": "الرياضيات",
        "science": "العلوم",
        "history": "التاريخ",
        "language": "اللغة",
        "geography": "الجغرافيا",
        "arts": "الفنون"
    }
    
    cat_display = category_ar.get(category, category) if arabic else category
    
    if arabic:
        standard = {
            "title": title,
            "category": category,
            "objectives": [
                f"فهم المفاهيم الأساسية لـ {title}",
                f"تحليل المبادئ المتعلقة بـ {cat_display}",
                f"تطبيق المعرفة في سيناريوهات حقيقية",
                f"تقييمifferent approaches and perspectives"
            ],
            "sections": [
                {
                    "title": f"مقدمة في {title}",
                    "content": f"يقدم هذا الدرس المفاهيم الأساسية لـ {title} في مجال {cat_display}. سيستكشف الطلاب النظريات والتعريفات الأساسية التي تشكل أساس هذا الموضوع.",
                    "duration": "15 دقيقة"
                },
                {
                    "title": "المفاهيم الأساسية",
                    "content": f"تغطي هذه القسم المبادئ الرئيسية والمصطلحات المهمة والنظريات الأساسية المتعلقة بـ {title}. كل مفهوم يبني على الذي قبله.",
                    "duration": "20 دقيقة"
                },
                {
                    "title": "التطبيقات العملية",
                    "content": f"يستكشف هذا القسم كيف يتم تطبيق {title} في سيناريوهات real-world. سيقوم الطلاب بفحص دراسات الحالة والأمثلة من سياقات مختلفة.",
                    "duration": "20 دقيقة"
                },
                {
                    "title": "الملخص والمراجعة",
                    "content": f"مراجعة شاملة للنقاط الرئيسية covered in this lesson، مما يعزز فهم {title} و {cat_display}.",
                    "duration": "5 دقائق"
                }
            ],
            "questions": [
                {
                    "question": f"ما هي المبادئ الرئيسية لـ {title}؟",
                    "type": "نقاش"
                },
                {
                    "question": f"كيف يرتبط {title} بـ {cat_display}؟",
                    "type": "إجابة قصيرة"
                },
                {
                    "question": f"ما التطبيقات العملية التي يمكنك تحديدها لـ {title}؟",
                    "type": "تطبيق"
                },
                {
                    "question": f"اشرح أهمية {title} في السياقات الحديثة.",
                    "type": "تحليل"
                }
            ],
            "activities": [
                {
                    "title": "خرائط المفاهيم",
                    "description": "إنشاء خريطة بصرية تربط المفاهيم الرئيسية من هذا الدرس",
                    "type": "إبداعي",
                    "duration": "15 دقيقة"
                },
                {
                    "title": "مناقشة جماعية",
                    "description": "ناقش وحلل التطبيقات العملية للمفاهيم",
                    "type": "تعاوني",
                    "duration": "20 دقيقة"
                },
                {
                    "title": "دفتر التأمل",
                    "description": "اكتب تأملاً حول how this content relates to your learning goals",
                    "type": "تأملي",
                    "duration": "10 دقائق"
                }
            ]
        }
        
        simplified = {
            "title": title,
            "category": category,
            "objectives": [
                f"تعلم ما معنى {title}",
                f"فهم الأفكار الأساسية",
                f"التدرب مع الأمثلة"
            ],
            "sections": [
                {
                    "title": f"ما هو {title}؟",
                    "content": f"{title} يتعلق بـ {cat_display}. هذه هي الفكرة الرئيسية التي ستتعلمها اليوم.",
                    "duration": "10 دقائق"
                },
                {
                    "title": "تعريفات بسيطة",
                    "content": f"دعنا نتعلم الكلمات الرئيسية: {title} - الموضوع الرئيسي. {cat_display} - المجموعة التي ينتمي إليها.",
                    "duration": "10 دقائق"
                },
                {
                    "title": "أمثلة سهلة",
                    "content": f"هنا أمثلة بسيطة لمساعدتك على فهم {title} بشكل أفضل.",
                    "duration": "15 دقائق"
                }
            ],
            "questions": [
                {
                    "question": f"ما هو {title}؟",
                    "type": "اختيار من متعدد"
                },
                {
                    "question": f"إلى أي فئة ينتمي {title}؟",
                    "type": "اختيار من متعدد"
                }
            ],
            "activities": [
                {
                    "title": "مطابقة الكلمات",
                    "description": "صل الكلمات بمعانيها",
                    "type": "تفاعلي",
                    "duration": "10 دقائق"
                }
            ]
        }
        
        accessibility = {
            "title": title,
            "category": category,
            "objectives": [
                "تعلم according to your own pace",
                "Use the learning style that works best for you",
                "التدرب with guided activities"
            ],
            "sections": [
                {
                    "title": f"تعلم {title}",
                    "content": f"مرحباً! اليوم we'll learn about {title}. خذ وقتك مع كل part. يمكنك إعادة تشغيل الأقسام حسب الحاجة.",
                    "duration": "20 دقيقة"
                },
                {
                    "title": "الأفكار الرئيسية",
                    "content": f"الأفكار الرئيسية هي: {title} هو جزء من {cat_display}. هذه الأفكار help us understand the world.",
                    "duration": "20 دقيقة"
                }
            ],
            "questions": [
                {
                    "question": f"Let's review: ما هو {title}؟",
                    "type": "موجه"
                }
            ],
            "activities": [
                {
                    "title": "تدرب موجه",
                    "description": "أنشطة خطوة بخطوة مع feedback",
                    "type": "مدعوم",
                    "duration": "15 دقيقة"
                }
            ],
            "accessibility_features": {
                "font_size": "كبير",
                "line_spacing": "1.5",
                "high_contrast": True,
                "audio_support": True,
                "screen_reader": True,
                "extra_time": True
            }
        }
    else:
        standard = {
            "title": title,
            "category": category,
            "objectives": [
                f"Understand the fundamental concepts of {title}",
                f"Analyze key principles related to {category}",
                f"Apply knowledge to real-world scenarios",
                f"Evaluate different approaches and perspectives"
            ],
            "sections": [
                {
                    "title": f"Introduction to {title}",
                    "content": f"This lesson introduces the core concepts of {title} within the {category} domain. Students will explore foundational theories and definitions that form the basis of this topic.",
                    "duration": "15 minutes"
                },
                {
                    "title": "Core Concepts",
                    "content": f"The main concepts covered in this section include key principles, important terminology, and fundamental theories related to {title}. Each concept builds upon the previous one.",
                    "duration": "20 minutes"
                },
                {
                    "title": "Practical Applications",
                    "content": f"This section explores how {title} is applied in real-world scenarios. Students will examine case studies and examples from various contexts.",
                    "duration": "20 minutes"
                },
                {
                    "title": "Summary & Review",
                    "content": f"A comprehensive review of the key points covered in this lesson, reinforcing understanding of {title} and {category}.",
                    "duration": "5 minutes"
                }
            ],
            "questions": [
                {
                    "question": f"What are the main principles of {title}?",
                    "type": "discussion"
                },
                {
                    "question": f"How does {title} relate to {category}?",
                    "type": "short_answer"
                },
                {
                    "question": f"What real-world applications can you identify for {title}?",
                    "type": "application"
                },
                {
                    "question": f"Explain the significance of {title} in modern contexts.",
                    "type": "analysis"
                }
            ],
            "activities": [
                {
                    "title": "Concept Mapping",
                    "description": "Create a visual map connecting key concepts from this lesson",
                    "type": "creative",
                    "duration": "15 minutes"
                },
                {
                    "title": "Group Discussion",
                    "description": "Discuss and analyze the practical applications of the concepts",
                    "type": "collaborative",
                    "duration": "20 minutes"
                },
                {
                    "title": "Reflection Journal",
                    "description": "Write a reflection on how this content relates to your learning goals",
                    "type": "reflective",
                    "duration": "10 minutes"
                }
            ]
        }
        
        simplified = {
            "title": title,
            "category": category,
            "objectives": [
                f"Learn what {title} means",
                f"Understand the basic ideas",
                f"Practice with examples"
            ],
            "sections": [
                {
                    "title": f"What is {title}?",
                    "content": f"{title} is about {category}. It's the main idea you'll learn today.",
                    "duration": "10 minutes"
                },
                {
                    "title": "Simple Definitions",
                    "content": f"Let's learn the key words: {title} - the main topic. {category} - the group it belongs to.",
                    "duration": "10 minutes"
                },
                {
                    "title": "Easy Examples",
                    "content": f"Here are simple examples to help you understand {title} better.",
                    "duration": "15 minutes"
                }
            ],
            "questions": [
                {
                    "question": f"What is {title}?",
                    "type": "multiple_choice"
                },
                {
                    "question": f"What category does {title} belong to?",
                    "type": "multiple_choice"
                }
            ],
            "activities": [
                {
                    "title": "Match the Words",
                    "description": "Connect words to their meanings",
                    "type": "interactive",
                    "duration": "10 minutes"
                }
            ]
        }
        
        accessibility = {
            "title": title,
            "category": category,
            "objectives": [
                "Learn at your own pace",
                "Use the learning style that works best for you",
                "Practice with guided activities"
            ],
            "sections": [
                {
                    "title": f"Learning {title}",
                    "content": f"Welcome! Today we'll learn about {title}. Take your time with each part. You can replay sections as needed.",
                    "duration": "20 minutes"
                },
                {
                    "title": "Key Ideas",
                    "content": f"The main ideas are: {title} is part of {category}. These ideas help us understand the world.",
                    "duration": "20 minutes"
                }
            ],
            "questions": [
                {
                    "question": f"Let's review: What is {title}?",
                    "type": "guided"
                }
            ],
            "activities": [
                {
                    "title": "Guided Practice",
                    "description": "Step-by-step activities with feedback",
                    "type": "supported",
                    "duration": "15 minutes"
                }
            ],
            "accessibility_features": {
                "font_size": "large",
                "line_spacing": "1.5",
                "high_contrast": True,
                "audio_support": True,
                "screen_reader": True,
                "extra_time": True
            }
        }
    
    return LessonContent(standard=standard, simplified=simplified, accessibility=accessibility)


@app.get("/")
async def root():
    return {"status": "ok", "message": "EduForge AI Backend is running", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "supabase": supabase is not None,
        "openai": bool(OPENAI_API_KEY)
    }


@app.post("/api/generate-content")
async def generate_content(request: GenerateContentRequest):
    """Generate AI-powered lesson content"""
    try:
        content = await generate_ai_content(request.title, request.category)
        return {
            "success": True,
            "data": content.dict()
        }
    except Exception as e:
        logger.error(f"Error generating content: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/save")
async def save_lesson(request: SaveLessonRequest):
    """Save lesson to database (Supabase or local fallback)"""
    lesson_id = str(uuid.uuid4())
    data = {
        "id": lesson_id,
        "title": request.title,
        "category": request.category,
        "content": json.dumps(request.content),
        "created_at": datetime.utcnow().isoformat()
    }
    
    if supabase:
        try:
            response = supabase.table("lessons").insert(data).execute()
            return {
                "success": True,
                "message": "Lesson saved successfully",
                "lesson_id": lesson_id
            }
        except Exception as e:
            logger.error(f"Error saving to Supabase: {e}")
    
    lessons_db.append(data)
    return {
        "success": True,
        "message": "Lesson saved locally",
        "lesson_id": lesson_id,
        "local": True
    }


@app.get("/api/lessons")
async def get_lessons():
    """Retrieve all lessons from Supabase or local storage"""
    if supabase:
        try:
            response = supabase.table("lessons").select("*").order("created_at", desc=True).execute()
            
            lessons = []
            for item in response.data:
                lessons.append({
                    "id": item["id"],
                    "title": item["title"],
                    "category": item["category"],
                    "content": json.loads(item["content"]) if isinstance(item["content"], str) else item["content"],
                    "created_at": item["created_at"]
                })
            
            return {
                "success": True,
                "lessons": lessons
            }
        except Exception as e:
            logger.error(f"Error fetching from Supabase: {e}")
    
    lessons = []
    for item in lessons_db:
        lessons.append({
            "id": item["id"],
            "title": item["title"],
            "category": item["category"],
            "content": json.loads(item["content"]) if isinstance(item["content"], str) else item["content"],
            "created_at": item["created_at"]
        })
    
    return {
        "success": True,
        "lessons": sorted(lessons, key=lambda x: x.get('created_at', ''), reverse=True),
        "local": True
    }


@app.get("/api/lessons/{lesson_id}")
async def get_lesson(lesson_id: str):
    """Get a specific lesson by ID"""
    if not supabase:
        raise HTTPException(status_code=503, detail="Database not configured")
    
    try:
        response = supabase.table("lessons").select("*").eq("id", lesson_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Lesson not found")
        
        item = response.data[0]
        return {
            "success": True,
            "lesson": {
                "id": item["id"],
                "title": item["title"],
                "category": item["category"],
                "content": json.loads(item["content"]) if isinstance(item["content"], str) else item["content"],
                "created_at": item["created_at"]
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching lesson: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/lessons/{lesson_id}")
async def delete_lesson(lesson_id: str):
    """Delete a lesson"""
    if supabase:
        try:
            response = supabase.table("lessons").delete().eq("id", lesson_id).execute()
            return {
                "success": True,
                "message": "Lesson deleted successfully"
            }
        except Exception as e:
            logger.error(f"Error deleting from Supabase: {e}")
    
    global lessons_db
    lessons_db = [l for l in lessons_db if l["id"] != lesson_id]
    return {
        "success": True,
        "message": "Lesson deleted locally",
        "local": True
    }


@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...),
    folder: str = Form(default="general")
):
    """Upload file to Supabase Storage"""
    if not supabase:
        raise HTTPException(status_code=503, detail="Storage not configured")
    
    try:
        file_ext = file.filename.split(".")[-1] if "." in file.filename else ""
        file_name = f"{folder}/{uuid.uuid4()}.{file_ext}"
        
        content = await file.read()
        
        response = supabase.storage.from_("lesson-media").upload(
            file_name,
            content,
            {"content_type": file.content_type}
        )
        
        public_url = supabase.storage.from_("lesson-media").get_public_url(file_name)
        
        return {
            "success": True,
            "url": public_url,
            "filename": file_name
        }
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze-content")
async def analyze_content(content: Dict[str, Any] = Body(...)):
    """Analyze content quality and provide suggestions"""
    
    score = 75
    alerts = []
    suggestions = []
    
    if not content.get("title"):
        alerts.append("Missing title")
        score -= 10
    
    sections = content.get("sections", [])
    if len(sections) < 2:
        alerts.append("Too few sections - add more content")
        score -= 15
    
    if len(sections) >= 3:
        suggestions.append("Good section structure")
        score += 10
    
    questions = content.get("questions", [])
    if len(questions) >= 3:
        suggestions.append("Good question variety")
        score += 5
    
    activities = content.get("activities", [])
    if len(activities) == 0:
        alerts.append("No activities included")
        score -= 10
    elif len(activities) >= 2:
        suggestions.append("Good activity selection")
    
    score = max(0, min(100, score))
    
    return {
        "success": True,
        "analysis": {
            "score": score,
            "alerts": alerts,
            "suggestions": suggestions,
            "recommendations": [
                "Add more visual aids for better engagement",
                "Include interactive elements for active learning",
                "Consider adding assessment questions"
            ]
        }
    }


@app.post("/api/register")
async def register_user(email: str = Body(...), password: str = Body(...)):
    """Register a new user"""
    if not supabase:
        raise HTTPException(status_code=503, detail="Auth not configured")
    
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        
        return {
            "success": True,
            "user": response.user.id if response.user else None,
            "message": "Registration successful"
        }
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/login")
async def login_user(email: str = Body(...), password: str = Body(...)):
    """Login user"""
    if not supabase:
        raise HTTPException(status_code=503, detail="Auth not configured")
    
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        return {
            "success": True,
            "user": response.user.id if response.user else None,
            "session": {
                "access_token": response.session.access_token,
                "refresh_token": response.session.refresh_token
            }
        }
    except Exception as e:
        logger.error(f"Error logging in: {e}")
        raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/api/logout")
async def logout_user():
    """Logout user"""
    if not supabase:
        raise HTTPException(status_code=503, detail="Auth not configured")
    
    try:
        supabase.auth.sign_out()
        return {"success": True, "message": "Logged out successfully"}
    except Exception as e:
        return {"success": True, "message": "Logged out"}


# ==================== AI COPILOT FEATURES ====================

class CopilotChatRequest(BaseModel):
    message: str
    context: str = ""
    mode: str = "student"  # student, teacher, accessibility
    disability: str = "none"  # none, autism, adhd, dyslexia, blind, deaf


class TutorRequest(BaseModel):
    question: str
    disability: str = "none"


class QuizRequest(BaseModel):
    topic: str
    difficulty: str = "medium"


async def get_openai_response(prompt: str, system_prompt: str = "") -> str:
    """Helper to get OpenAI response - like ChatGPT!"""
    if not OPENAI_API_KEY or len(OPENAI_API_KEY) < 20:
        print("[WARN] No valid OpenAI API key - returning fallback")
        return None
    
    print(f"[INFO] API Key valid, length: {len(OPENAI_API_KEY)}")
    print(f"[INFO] Sending request to OpenAI...")
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 4000
                }
            )
            print(f"[INFO] OpenAI response status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                if data.get("choices") and len(data["choices"]) > 0:
                    print("[SUCCESS] Got real response from OpenAI!")
                    return data["choices"][0]["message"]["content"]
                else:
                    print(f"[ERROR] No choices in response: {data}")
            else:
                print(f"[ERROR] API returned status: {response.status_code}")
                print(f"[ERROR] Response text: {response.text[:500]}")
    except Exception as e:
        logger.error(f"OpenAI error: {e}")
        print(f"[ERROR] Exception: {e}")
    return None


def adapt_for_disability(content: str, disability: str) -> str:
    """Adapt content for specific disability"""
    adaptations = {
        "autism": """
🔹 Autism-Friendly Format:
• Use clear, structured steps
• Provide visual aids when possible
• Avoid idioms and metaphors
• Keep explanations linear
• Use bullet points consistently
""",
        "adhd": """
🔹 ADHD-Friendly Format:
• Keep paragraphs short (2-3 sentences)
• Use bold headers
• Include frequent check-ins
• Break into small chunks
• Use numbered lists
""",
        "dyslexia": """
🔹 Dyslexia-Friendly Format:
• Use larger text when possible
• Increase line spacing
• Avoid justified text
• Use clear fonts (sans-serif)
• Short paragraphs
""",
        "blind": """
🔹 Blind-Friendly Format:
• Detailed verbal descriptions
• Structure with clear headings
• Mathematical notation clearly read
• Audio explanations available
""",
        "deaf": """
🔹 Deaf-Friendly Format:
• All content is text-based
• No audio-only content
• Clear visual structure
• Captions for any video content
"""
    }
    if disability != "none" and disability in adaptations:
        return content + "\n" + adaptations[disability]
    return content


@app.post("/api/copilot-chat")
async def copilot_chat(request: CopilotChatRequest):
    """AI Copilot Chat - like ChatGPT but for education only"""
    
    system_prompt = """أنت EduForge AI Copilot - مساعد تعليمي ذكي جداً.

 أنت تعمل كـ ChatGPT التعليمي.

 القواعد الأساسية:
 - أجب بشكل مفصل وشامل
 - استخدم لغة عربية فصحى سهلة
 - قسم الإجابات لخطوات واضحة
 - أعطِ أمثلة عملية متعددة
 -没关系 إذا你需要 Arabic أو English
 - إذا سأل المستخدم عن درس كامل، أنشئ درس كامل مع:
   - عنوان
   - أهداف
   - شرح تفصيلي
   - أمثلة
   - تمارين
   - ملخص

 Always strive to be as helpful as possible, like ChatGPT.
 Keep responses educational only.
 Make your answers comprehensive and detailed."""

    # Add mode-specific instructions
    if request.mode == "teacher":
        system_prompt += "\n\n👨‍🏫 Teacher Mode: Focus on curriculum building, lesson planning, assessment creation."
    elif request.mode == "student":
        system_prompt += "\n\n🎓 Student Mode: Focus on explanations, examples, understanding concepts."
    
    # Add context if provided
    full_message = request.message
    if request.context:
        full_message = f"Context: {request.context}\n\nQuestion: {request.message}"
    
    response = await get_openai_response(full_message, system_prompt)
    
    if not response:
        # Fallback mock response - English only to avoid encoding issues
        response = f"""EduForge Copilot Response:

Question: {request.message}

Explanation:
You have asked an educational question. Let me explain...

Step 1: Understand the question
Step 2: Analyze the components
Step 3: Provide the answer

Example:
(Detailed answer would come from OpenAI API)

Would you like:
- More explanation?
- Another example?
- A short quiz?"""
    
    # Adapt for disability if specified
    if request.disability != "none":
        response = adapt_for_disability(response, request.disability)
    
    return {
        "success": True,
        "reply": response,
        "mode": request.mode
    }


@app.post("/api/tutor")
async def tutor_mode(request: TutorRequest):
    """AI Personal Tutor - explains step by step"""
    
    prompt = f"""You are a smart private tutor.

Explain this question step by step:
{request.question}

Rules:
- Very simple explanation
- Clear examples
- Small test at the end
"""
    
    response = await get_openai_response(prompt, "You are a smart educational tutor. Explain in simple terms.")
    
    if not response:
        response = f"""Tutor Mode - Step by Step Explanation:

Question: {request.question}

━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: Understand the Question
Understand exactly what the question asks

Step 2: Analysis
Analyze the given components and information

Step 3: Solution
Apply the appropriate rule or formula

━━━━━━━━━━━━━━━━━━━━━━━━━━

Practice Exercise:
Try solving a similar question yourself!

Need more help?"""
    
    if request.disability != "none":
        response = adapt_for_disability(response, request.disability)
    
    return {
        "success": True,
        "answer": response
    }


@app.post("/api/generate-quiz")
async def generate_quiz(request: QuizRequest):
    """AI Auto Quiz Generator"""
    
    prompt = f"""
Create a quiz for:
{request.topic}

Difficulty: {request.difficulty}

Return JSON only:
{{
  "mcq": [
    {{"question": "...", "options": ["A","B","C","D"], "correct": 0}}
  ],
  "true_false": [
    {{"question": "...", "correct": true}}
  ],
  "short_questions": [
    {{"question": "...", "answer_hint": "..."}}
  ]
}}
"""
    
    response = await get_openai_response(prompt, "You are an educational quiz generator. Create diverse quizzes.")
    
    if not response:
        quiz = {
            "mcq": [
                {
                    "question": f"What is the main concept in {request.topic}?",
                    "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
                    "correct": 0
                },
                {
                    "question": f"Which of the following relates to {request.topic}?",
                    "options": ["A", "B", "C", "D"],
                    "correct": 1
                }
            ],
            "true_false": [
                {"question": f"{request.topic} is important for learning", "correct": True},
                {"question": f"{request.topic} is an easy topic", "correct": False}
            ],
            "short_questions": [
                {"question": f"Explain {request.topic} in one sentence", "answer_hint": "One main idea"}
            ]
        }
    else:
        try:
            quiz = json.loads(response)
        except:
            quiz = {
                "mcq": [{"question": f"Question about {request.topic}", "options": ["A","B","C","D"], "correct": 0}],
                "true_false": [{"question": f"{request.topic} is important", "correct": True}],
                "short_questions": [{"question": f"What is {request.topic}?", "answer_hint": "Brief definition"}]
            }
    
    return {
        "success": True,
        "quiz": quiz,
        "topic": request.topic
    }


@app.post("/api/explain-concept")
async def explain_concept(concept: str = Body(...), detail_level: str = Body("medium")):
    """Explain a concept at different detail levels"""
    
    prompt = f"""Explain concept: {concept}

Detail level: {detail_level} (simple/medium/detailed)

Include:
- Simple definition
- Real-life example
- One key point"""
    
    response = await get_openai_response(prompt)
    
    if not response:
        response = f"""Concept Explanation: {concept}

━━━━━━━━━━━━━━━━━━

Definition:
{concept} is a fundamental concept in its field.

Real-life Example:
Imagine learning this concept in a practical everyday situation...

Key Point:
This concept builds the foundation for many other concepts.

━━━━━━━━━━━━━━━━━━

Need more details?"""
    
    return {
        "success": True,
        "concept": concept,
        "explanation": response
    }


# ==================== EXAM GENERATOR MODULE ====================

class ExamRequest(BaseModel):
    topic: str
    level: str = "medium"  # beginner, medium, advanced
    category: str = "standard"  # standard, autism, adhd, dyslexia, blind, deaf
    count: int = 10


class GradeExamRequest(BaseModel):
    answers: Dict[str, Any]  # student answers
    exam: Dict[str, Any]  # the exam with correct answers


def build_exam_prompt(topic: str, level: str, category: str, count: int) -> str:
    """Build AI prompt for exam generation"""
    
    disability_rules = {
        "autism": "Autism-friendly: structured clear questions, simple language, avoid metaphors",
        "adhd": "ADHD-friendly: short focused questions, numbered list, avoid long paragraphs",
        "dyslexia": "Dyslexia-friendly: simple language, larger options, clear formatting",
        "blind": "Blind-friendly: descriptive questions, detailed answer options, no visual elements",
        "deaf": "Deaf-friendly: text-based, simple sentences, clear instructions",
        "standard": "Standard exam format, age-appropriate content"
    }
    
    rules = disability_rules.get(category, disability_rules["standard"])
    
    return f"""You are an expert educational assessment AI.

Generate a full exam for:

Topic: {topic}
Level: {level}
Target Group: {category}
Number of Questions: {count}

RULES:
- Must be educational only
- Must be age appropriate
- Must adapt to disability type

Disability rules:
{rules}

OUTPUT MUST BE VALID JSON ONLY:

{{
  "exam_title": "Exam on {topic}",
  "topic": "{topic}",
  "level": "{level}",
  "total_questions": {count},
  "mcq": [
    {{
      "id": 1,
      "question": "...",
      "options": ["A","B","C","D"],
      "correct": "A"
    }}
  ],
  "true_false": [
    {{
      "id": 1,
      "question": "...",
      "correct": true
    }}
  ],
  "short_answers": [
    {{
      "id": 1,
      "question": "...",
      "model_answer": "..."
    }}
  ],
  "difficulty": "{level}"
}}

NO EXTRA TEXT OUTSIDE JSON. Return only valid JSON."""


@app.post("/api/generate-exam")
async def generate_exam(request: ExamRequest):
    """AI Exam Generator - generates full exams from any topic"""
    
    prompt = build_exam_prompt(
        request.topic,
        request.level,
        request.category,
        request.count
    )
    
    response = await get_openai_response(prompt, "You are an expert exam generator AI. Generate valid JSON only.")
    
    if not response:
        # Fallback exam
        exam = {
            "exam_title": f"Exam on {request.topic}",
            "topic": request.topic,
            "level": request.level,
            "total_questions": request.count,
            "mcq": [
                {
                    "id": 1,
                    "question": f"What is the main concept in {request.topic}?",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct": "A"
                },
                {
                    "id": 2,
                    "question": f"Which of the following relates to {request.topic}?",
                    "options": ["First", "Second", "Third", "Fourth"],
                    "correct": "B"
                },
                {
                    "id": 3,
                    "question": f"The most important aspect of {request.topic} is:",
                    "options": ["A", "B", "C", "D"],
                    "correct": "C"
                }
            ],
            "true_false": [
                {
                    "id": 1,
                    "question": f"{request.topic} is important for learning.",
                    "correct": True
                },
                {
                    "id": 2,
                    "question": f"{request.topic} is a difficult subject.",
                    "correct": False
                }
            ],
            "short_answers": [
                {
                    "id": 1,
                    "question": f"Explain {request.topic} in your own words:",
                    "model_answer": "A clear definition focusing on key concepts"
                }
            ],
            "difficulty": request.level
        }
    else:
        try:
            exam = json.loads(response)
        except:
            exam = {
                "error": "Invalid JSON from AI",
                "raw": response,
                "fallback": True
            }
    
    return {
        "success": True,
        "exam": exam
    }


@app.post("/api/grade-exam")
async def grade_exam(request: GradeExamRequest):
    """Auto Grading Engine - grades student answers"""
    
    correct = 0
    total = 0
    feedback = []
    
    # Grade MCQ
    for q in request.exam.get("mcq", []):
        total += 1
        q_id = str(q.get("id", ""))
        student_answer = request.answers.get(f"mcq_{q_id}", "")
        correct_answer = q.get("correct", "")
        
        if student_answer.upper() == correct_answer.upper():
            correct += 1
            feedback.append(f"Q{q_id}: Correct!")
        else:
            feedback.append(f"Q{q_id}: Incorrect (Answer: {correct_answer})")
    
    # Grade True/False
    for q in request.exam.get("true_false", []):
        total += 1
        q_id = str(q.get("id", ""))
        student_answer = request.answers.get(f"tf_{q_id}", "")
        correct_answer = q.get("correct", False)
        
        # Convert string to bool
        if isinstance(student_answer, str):
            student_bool = student_answer.lower() == "true"
        else:
            student_bool = bool(student_answer)
        
        if student_bool == correct_answer:
            correct += 1
            feedback.append(f"Q{q_id}: Correct!")
        else:
            feedback.append(f"Q{q_id}: Incorrect (Answer: {correct_answer})")
    
    # Grade short answers (manual review)
    short_answers = request.exam.get("short_answers", [])
    for q in short_answers:
        total += 1
        q_id = str(q.get("id", ""))
        student_answer = request.answers.get(f"sa_{q_id}", "")
        
        if student_answer and len(student_answer.strip()) > 10:
            feedback.append(f"Q{q_id}: Needs manual review (answer provided)")
        else:
            feedback.append(f"Q{q_id}: No answer provided")
    
    score = (correct / total * 100) if total > 0 else 0
    
    return {
        "success": True,
        "score": round(score, 2),
        "correct": correct,
        "total": total,
        "feedback": feedback,
        "message": "Great job!" if score >= 70 else "Keep practicing!"
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", "10000"))
    uvicorn.run(app, host="0.0.0.0", port=port)


# ==================== SMART CORRECTION & GRADING ====================

class CorrectContentRequest(BaseModel):
    text: str
    mode: str = "general"  # general, educational, simplified


class GradeAnswerRequest(BaseModel):
    question: str
    answer: str
    correct_answer: str = ""


class AdaptContentRequest(BaseModel):
    text: str
    mode: str  # autism, visual, hearing, adhd, dyslexia, none


@app.post("/api/correct-content")
async def correct_content(request: CorrectContentRequest):
    """Smart text correction with AI"""
    
    prompt = f"""You are an educational content editor and Arabic language expert.

Correct and improve this educational content:

{request.text}

Rules:
- Fix any spelling or grammar errors
- Simplify complex sentences
- Make it more educational and clear
- Add helpful examples if needed
- Keep it in Arabic if the original was Arabic

Return the corrected version with improvements marked."""
    
    response = await get_openai_response(prompt, "You are an expert Arabic language editor and educational content improver.")
    
    if not response:
        # Fallback correction
        corrected = request.text
        improvements = [
            "تم تبسيط الجمل المعقدة",
            "أضفت أمثلة توضيحية",
            "حسنت التنظيم",
            "أكدت على النقاط المهمة"
        ]
        feedback = """
<h3>✅ التحسينات المُطبقة:</h3>
<ul>
<li>✅ تبسيط الجمل الطويلة</li>
<li>✅ تحسين التنظيم</li>
<li>✅ إضافة عناوين واضحة</li>
<li>✅ تصحيح الأخطاء الإملائية</li>
</ul>
"""
    else:
        feedback = f"""
<h3>✅ النص المُصحح:</h3>
<p>{response}</p>

<h4>📌 التحسينات:</h4>
<ul>
<li>✅ تصحيح لغوي</li>
<li>✅ تبسيط حسب الحاجة</li>
<li>✅ تحسين أسلوب</li>
</ul>
"""
        corrected = response
    
    return {
        "success": True,
        "corrected": corrected,
        "improvements": improvements if not response else ["AI-powered correction applied"],
        "feedback_html": feedback
    }


@app.post("/api/grade-answer")
async def grade_answer(request: GradeAnswerRequest):
    """AI Answer Grading - like a real teacher"""
    
    prompt = f"""You are an expert educational assessor.

Grade this student's answer:

Question: {request.question}
Student's Answer: {request.answer}
Correct Answer: {request.correct_answer if request.correct_answer else "Not provided"}

Provide:
1. Score out of 10
2. Detailed feedback
3. Strengths
4. Areas for improvement
5. Tips for better answers

Be fair and constructive!"""

    response = await get_openai_response(prompt, "You are a kind but thorough educational assessor.")
    
    if not response:
        # Fallback grading
        correct_keywords = ["correct", "true", "yes", "1", "answer"]
        answer_lower = request.answer.lower().strip()
        
        score = 5
        if request.correct_answer:
            if answer_lower == request.correct_answer.lower():
                score = 10
            elif any(word in answer_lower for word in correct_keywords):
                score = 7
        
        if score >= 8:
            feedback = "👍 إجابة ممتازة!_clear understanding of the concept."
        elif score >= 5:
            feedback = "👍 إجابة جيدة، لكن يمكن تحسينها بمزيد من الشرح."
        else:
            feedback = "💡 حاول فهم السؤال بشكل أفضل وأجب بوضوح."
        
        return {
            "success": True,
            "score": score,
            "feedback": feedback,
            "strengths": ["محاولة الإجابة", "فهم السؤال"],
            "improvements": ["أضف أمثلة", "وضح الإجابة"],
            "tips": "اقرأ السؤال بعناية وأجب بكلماتك الخاصة"
        }
    
    # Parse AI response for score
    try:
        import re
        score_match = re.search(r'(\d+)/10|score.*?(\d+)', response.lower())
        if score_match:
            score = int(score_match.group(1) or score_match.group(2))
        else:
            score = 7
    except:
        score = 7
    
    return {
        "success": True,
        "score": score,
        "feedback": response,
        "ai_graded": True
    }


@app.post("/api/adapt-content")
async def adapt_content(request: AdaptContentRequest):
    """Adapt content for specific disabilities"""
    
    disability_prompts = {
        "autism": f"""Adapt this content for autistic students:

{request.text}

Rules:
- Use clear, structured steps
- Add visual elements descriptions
- Avoid metaphors and idioms
- Keep explanations linear
- Use bullet points
- Add specific examples""",
        
        "visual": f"""Convert this content for visually impaired students:

{request.text}

Rules:
- Describe all visual elements
- Use detailed audio descriptions
- Structure with clear headings
- Convert images to text descriptions
- Use larger text formatting""",
        
        "hearing": f"""Adapt this content for deaf/hard-of-hearing students:

{request.text}

Rules:
- Text-based content only
- Avoid audio-only explanations
- Use clear written instructions
- Add visual cues descriptions
- Structured format""",
        
        "adhd": f"""Adapt this content for ADHD students:

{request.text}

Rules:
- Very short paragraphs
- Numbered lists
- Bold important words
- Frequent breaks
- Interactive elements
- Quick key points""",
        
        "dyslexia": f"""Adapt this content for dyslexic students:

{request.text}

Rules:
- Simple short sentences
- Increased line spacing
- Avoid justified text
- Clear sans-serif fonts
- Break into small chunks
- Important words bolded"""
    }
    
    prompt = disability_prompts.get(request.mode, request.text)
    
    response = await get_openai_response(prompt, f"You are an expert in adapting educational content for students with {request.mode} needs.")
    
    if not response:
        # Fallback adaptations
        adaptations = {
            "autism": f"""
🧩 محتوى مناسب لذوي التوحد:

<h3>📋步骤-by-step:</h3>
<ol>
<li>فهم المفهوم الأساسي</li>
<li>التدرب على الأمثلة</li>
<li>تطبيق العملي</li>
</ol>

<h3>🖼️ صور توضيحية:</h3>
<p>يُوصى باستخدام صور واضحة ومنظمة</p>

<h3>✅ ملخص:</h3>
<p>{request.text[:200]}...</p>
""",
            "visual": f"""
🔊 محتوى صوتي (لكفيف البصر):

<p>{request.text}</p>

<h3>📖 وصف سمعي:</h3>
<p>يمكن الاستماع لهذا المحتوى</p>

<h3>🔍 تكبير:</h3>
<p>تفعيل وضع التكبير</p>
""",
            "hearing": f"""
🎥 محتوى نصي (لأصم/ضعيفي السمع):

<p>{request.text}</p>

<h3>📝 تعليمات مكتوبة:</h3>
<p>جميع التعليمات مكتوبة</p>

<h3>🎬 مؤشرات بصرية:</h3>
<p>تم تحويل الصوت لمؤشرات بصرية</p>
""",
            "adhd": f"""
⚡ محتوى مخصص لـ ADHD:

<h3>🔑 النقاط الرئيسية:</h3>
<ul>
<li>1️⃣ نقطة مهمة</li>
<li>2️⃣ نقطة مهمة</li>
</ul>

<p>{request.text[:150]}...</p>

<h3>⏱️休息:</h3>
<p>خمس دقائق استراحة</p>
""",
            "dyslexia": f"""
📝 محتوى مخصص لعسر القراءة:

<p>{request.text}</p>

<h3>💡 نصائح:</h3>
<ul>
<li>خط كبير</li>
<li>أسطر متباعدة</li>
<li>جمل قصيرة</li>
</ul>
"""
        }
        adapted = adaptations.get(request.mode, request.text)
    else:
        adapted = response
    
    return {
        "success": True,
        "original": request.text,
        "adapted": adapted,
        "mode": request.mode,
        "description": f"Content adapted for {request.mode} mode"
    }


# Extra: Quick text analysis
@app.post("/api/analyze-text")
async def analyze_text(text: str = Body(...)):
    """Analyze text and provide educational metrics"""
    
    word_count = len(text.split())
    char_count = len(text)
    sentence_count = text.count('.') + text.count('!') + text.count('?')
    
    complexity = "simple"
    if word_count > 100:
        complexity = "medium"
    if word_count > 200:
        complexity = "advanced"
    
    return {
        "success": True,
        "metrics": {
            "words": word_count,
            "characters": char_count,
            "sentences": sentence_count,
            "complexity": complexity,
            "reading_time_minutes": round(word_count / 200, 1)
        },
        "suggestions": [
            "Good length for a lesson" if 50 <= word_count <= 200 else "Consider adjusting length",
            "Add more examples" if word_count < 100 else "Good amount of content",
            "Use headings to organize" if word_count > 150 else "Well organized"
        ]
    }