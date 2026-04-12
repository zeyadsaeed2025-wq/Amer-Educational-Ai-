"""
Database module supporting SQLite, Supabase, and Railway PostgreSQL.
"""
import os
import json
import logging
from typing import Optional, List

logger = logging.getLogger(__name__)

# Check database configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")  # Railway PostgreSQL

USE_SUPABASE = bool(SUPABASE_URL and SUPABASE_KEY)
USE_POSTGRES = bool(DATABASE_URL and not USE_SUPABASE)


class DatabaseManager:
    """Database manager supporting SQLite, Supabase, and PostgreSQL."""
    
    def __init__(self):
        self._sqlite = None
        self._client = None
        self._engine = None
        self._SessionLocal = None
        
        if USE_POSTGRES:
            logger.info("Using Railway PostgreSQL")
            self._init_postgres()
        elif USE_SUPABASE:
            logger.info("Using Supabase")
            self._init_supabase()
        else:
            logger.info("Using SQLite (local development)")
            self._init_sqlite()
    
    def _init_sqlite(self):
        """Initialize SQLite connection."""
        try:
            from sqlalchemy import create_engine
            from sqlalchemy.orm import sessionmaker
            from sqlalchemy.ext.declarative import declarative_base
            
            self._engine = create_engine(
                "sqlite:///./eduforge.db",
                connect_args={"check_same_thread": False}
            )
            self._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)
            self._Base = declarative_base()
            self._create_tables_sqlite()
            logger.info("SQLite initialized")
        except Exception as e:
            logger.error(f"SQLite init error: {e}")
            raise
    
    def _init_postgres(self):
        """Initialize Railway PostgreSQL connection."""
        try:
            from sqlalchemy import create_engine
            from sqlalchemy.orm import sessionmaker
            from sqlalchemy.ext.declarative import declarative_base
            
            self._engine = create_engine(DATABASE_URL)
            self._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)
            self._Base = declarative_base()
            self._create_tables_postgres()
            logger.info("PostgreSQL initialized")
        except Exception as e:
            logger.error(f"PostgreSQL init error: {e}")
            self._init_sqlite()
    
    def _init_supabase(self):
        """Initialize Supabase connection."""
        try:
            from supabase import create_client
            self._client = create_client(SUPABASE_URL, SUPABASE_KEY)
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
        
        class Lesson(self._Base):
            __tablename__ = "lessons"
            id = Column(String, primary_key=True)
            title = Column(String)
            category = Column(String)
            content_standard = Column(Text)
            content_simplified = Column(Text)
            content_accessibility = Column(Text)
            ui_hints = Column(Text)
            created_at = Column(DateTime)
            updated_at = Column(DateTime)
        
        self._Base.metadata.create_all(bind=self._engine)
        self._Lesson = Lesson
    
    def _create_tables_postgres(self):
        """Create PostgreSQL tables."""
        from sqlalchemy import Column, String, DateTime, Text, text
        
        class Lesson(self._Base):
            __tablename__ = "lessons"
            id = Column(String(50), primary_key=True)
            title = Column(String(500))
            category = Column(String(50))
            content_standard = Column(Text)
            content_simplified = Column(Text)
            content_accessibility = Column(Text)
            ui_hints = Column(Text)
            created_at = Column(DateTime, server_default=text("NOW()"))
            updated_at = Column(DateTime, server_default=text("NOW()"))
        
        self._Base.metadata.create_all(bind=self._engine)
        self._Lesson = Lesson
    
    # SQL Operations (SQLite & PostgreSQL)
    def _create_lesson_sql(self, session, lesson_id: str, title: str, category: str, content: dict):
        """Create lesson in SQL database."""
        from datetime import datetime
        
        lesson = self._Lesson(
            id=lesson_id,
            title=title,
            category=category,
            content_standard=json.dumps(content.get("standard", {})),
            content_simplified=json.dumps(content.get("simplified", {})),
            content_accessibility=json.dumps(content.get("accessibility", {})),
            ui_hints=json.dumps(content.get("ui_hints", {})),
            created_at=datetime.utcnow(),
        )
        session.add(lesson)
        session.commit()
        return lesson_id
    
    def _get_lesson_sql(self, session, lesson_id: str) -> Optional[dict]:
        """Get lesson from SQL database."""
        lesson = session.query(self._Lesson).filter(self._Lesson.id == lesson_id).first()
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
    
    def _get_all_lessons_sql(self, session, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get all lessons from SQL database."""
        lessons = session.query(self._Lesson).order_by(self._Lesson.created_at.desc()).offset(skip).limit(limit).all()
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
    def _create_lesson_supabase(self, lesson_id: str, title: str, category: str, content: dict) -> str:
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
        self._client.table("lessons").insert(data).execute()
        return lesson_id
    
    def _get_lesson_supabase(self, lesson_id: str) -> Optional[dict]:
        """Get lesson from Supabase."""
        try:
            response = self._client.table("lessons").select("*").eq("id", lesson_id).execute()
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
    
    def _get_all_lessons_supabase(self, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get all lessons from Supabase."""
        try:
            response = self._client.table("lessons").select("id,title,category,created_at").range(skip, skip + limit - 1).execute()
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
            return self._create_lesson_supabase(lesson_id, title, category, content)
        elif self._SessionLocal:
            session = self._SessionLocal()
            try:
                return self._create_lesson_sql(session, lesson_id, title, category, content)
            finally:
                session.close()
        else:
            raise Exception("No database configured")
    
    def get_lesson(self, lesson_id: str) -> Optional[dict]:
        """Get lesson by ID (auto-detects database)."""
        if USE_SUPABASE:
            return self._get_lesson_supabase(lesson_id)
        elif self._SessionLocal:
            session = self._SessionLocal()
            try:
                return self._get_lesson_sql(session, lesson_id)
            finally:
                session.close()
        return None
    
    def get_all_lessons(self, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get all lessons (auto-detects database)."""
        if USE_SUPABASE:
            return self._get_all_lessons_supabase(skip, limit)
        elif self._SessionLocal:
            session = self._SessionLocal()
            try:
                return self._get_all_lessons_sql(session, skip, limit)
            finally:
                session.close()
        return []
    
    def get_session(self):
        """Get SQLAlchemy session."""
        if self._SessionLocal:
            return self._SessionLocal()
        return None


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
