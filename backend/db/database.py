"""
Database module supporting both SQLite (local) and Supabase (production).
"""
import os
import json
import logging
from typing import Optional, List, Dict
from datetime import datetime
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# Check if Supabase is configured
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

USE_SUPABASE = bool(SUPABASE_URL and SUPABASE_KEY)


class DatabaseManager:
    """Database manager that switches between SQLite and Supabase."""
    
    def __init__(self):
        self._sqlite = None
        self._supabase = None
        
        if USE_SUPABASE:
            logger.info("Using Supabase database")
            self._init_supabase()
        else:
            logger.info("Using SQLite database (local development)")
            self._init_sqlite()
    
    def _init_sqlite(self):
        """Initialize SQLite connection."""
        try:
            from sqlalchemy import create_engine
            from sqlalchemy.orm import sessionmaker
            from sqlalchemy.ext.declarative import declarative_base
            
            self.engine = create_engine(
                "sqlite:///./eduforge.db",
                connect_args={"check_same_thread": False}
            )
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            self.Base = declarative_base()
            
            # Create tables
            self._create_tables_sqlite()
            logger.info("SQLite initialized")
        except Exception as e:
            logger.error(f"SQLite init error: {e}")
            raise
    
    def _init_supabase(self):
        """Initialize Supabase connection."""
        try:
            from supabase import create_client
            
            self.client = create_client(SUPABASE_URL, SUPABASE_KEY)
            self._create_tables_supabase()
            logger.info("Supabase initialized")
        except ImportError:
            logger.warning("supabase-py not installed, falling back to SQLite")
            self._init_sqlite()
        except Exception as e:
            logger.error(f"Supabase init error: {e}")
            self._init_sqlite()
    
    def _create_tables_sqlite(self):
        """Create SQLite tables."""
        from sqlalchemy import Column, String, DateTime, Text
        
        class Lesson(self.Base):
            __tablename__ = "lessons"
            id = Column(String, primary_key=True)
            title = Column(String)
            category = Column(String)
            content_standard = Column(Text)
            content_simplified = Column(Text)
            content_accessibility = Column(Text)
            ui_hints = Column(Text)
            created_at = Column(DateTime, default=datetime.utcnow)
            updated_at = Column(DateTime, default=datetime.utcnow)
        
        self.Base.metadata.create_all(bind=self.engine)
        self.Lesson = Lesson
    
    def _create_tables_supabase(self):
        """Create Supabase tables via client."""
        # Tables will be created in Supabase dashboard
        # This just verifies connection
        try:
            self.client.table("lessons").select("id").limit(1).execute()
        except:
            logger.warning("Lessons table may not exist in Supabase")
    
    # SQLite Operations
    def create_lesson_sqlite(self, session, lesson_id: str, title: str, category: str, content: dict) -> str:
        """Create lesson in SQLite."""
        from datetime import datetime
        from sqlalchemy import Column, String, DateTime, Text
        
        lesson = self.Lesson(
            id=lesson_id,
            title=title,
            category=category,
            content_standard=json.dumps(content.get("standard", {})),
            content_simplified=json.dumps(content.get("simplified", {})),
            content_accessibility=json.dumps(content.get("accessibility", {})),
            ui_hints=json.dumps(content.get("ui_hints", {})),
        )
        session.add(lesson)
        session.commit()
        return lesson_id
    
    def get_lesson_sqlite(self, session, lesson_id: str) -> Optional[dict]:
        """Get lesson from SQLite."""
        lesson = session.query(self.Lesson).filter(self.Lesson.id == lesson_id).first()
        if lesson:
            return {
                "id": lesson.id,
                "title": lesson.title,
                "category": lesson.category,
                "standard": json.loads(lesson.content_standard) if lesson.content_standard else {},
                "simplified": json.loads(lesson.content_simplified) if lesson.content_simplified else {},
                "accessibility": json.loads(lesson.content_accessibility) if lesson.content_accessibility else {},
                "ui_hints": json.loads(lesson.ui_hints) if lesson.ui_hints else {},
            }
        return None
    
    def get_all_lessons_sqlite(self, session, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get all lessons from SQLite."""
        lessons = session.query(self.Lesson).offset(skip).limit(limit).all()
        return [
            {
                "id": l.id,
                "title": l.title,
                "category": l.category,
                "created_at": l.created_at.isoformat() if l.created_at else None,
            }
            for l in lessons
        ]
    
    # Supabase Operations
    def create_lesson_supabase(self, lesson_id: str, title: str, category: str, content: dict) -> str:
        """Create lesson in Supabase."""
        data = {
            "id": lesson_id,
            "title": title,
            "category": category,
            "content_standard": json.dumps(content.get("standard", {})),
            "content_simplified": json.dumps(content.get("simplified", {})),
            "content_accessibility": json.dumps(content.get("accessibility", {})),
            "ui_hints": json.dumps(content.get("ui_hints", {})),
        }
        self.client.table("lessons").insert(data).execute()
        return lesson_id
    
    def get_lesson_supabase(self, lesson_id: str) -> Optional[dict]:
        """Get lesson from Supabase."""
        try:
            response = self.client.table("lessons").select("*").eq("id", lesson_id).execute()
            if response.data:
                data = response.data[0]
                return {
                    "id": data["id"],
                    "title": data["title"],
                    "category": data["category"],
                    "standard": json.loads(data["content_standard"]) if data.get("content_standard") else {},
                    "simplified": json.loads(data["content_simplified"]) if data.get("content_simplified") else {},
                    "accessibility": json.loads(data["content_accessibility"]) if data.get("content_accessibility") else {},
                    "ui_hints": json.loads(data["ui_hints"]) if data.get("ui_hints") else {},
                }
        except Exception as e:
            logger.error(f"Supabase get error: {e}")
        return None
    
    def get_all_lessons_supabase(self, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get all lessons from Supabase."""
        try:
            response = self.client.table("lessons").select("id,title,category,created_at").range(skip, skip + limit - 1).execute()
            return [
                {
                    "id": l["id"],
                    "title": l["title"],
                    "category": l["category"],
                    "created_at": l.get("created_at"),
                }
                for l in response.data
            ]
        except Exception as e:
            logger.error(f"Supabase list error: {e}")
            return []
    
    # Unified Interface
    def create_lesson(self, lesson_id: str, title: str, category: str, content: dict) -> str:
        """Create lesson (auto-detects database)."""
        if USE_SUPABASE:
            return self.create_lesson_supabase(lesson_id, title, category, content)
        else:
            session = self.SessionLocal()
            try:
                return self.create_lesson_sqlite(session, lesson_id, title, category, content)
            finally:
                session.close()
    
    def get_lesson(self, lesson_id: str) -> Optional[dict]:
        """Get lesson by ID (auto-detects database)."""
        if USE_SUPABASE:
            return self.get_lesson_supabase(lesson_id)
        else:
            session = self.SessionLocal()
            try:
                return self.get_lesson_sqlite(session, lesson_id)
            finally:
                session.close()
    
    def get_all_lessons(self, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get all lessons (auto-detects database)."""
        if USE_SUPABASE:
            return self.get_all_lessons_supabase(skip, limit)
        else:
            session = self.SessionLocal()
            try:
                return self.get_all_lessons_sqlite(session, skip, limit)
            finally:
                session.close()
    
    def get_session(self):
        """Get SQLite session (for SQLAlchemy dependencies)."""
        if USE_SUPABASE:
            return None
        return self.SessionLocal()


# Global database manager
db_manager = DatabaseManager()


def get_db():
    """FastAPI dependency for database session."""
    session = db_manager.get_session()
    if session:
        try:
            yield session
        finally:
            session.close()
    else:
        yield None
