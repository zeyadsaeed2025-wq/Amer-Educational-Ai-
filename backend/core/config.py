import os
from functools import lru_cache


class Settings:
    """Application settings from environment variables."""
    
    def __init__(self):
        self.app_name = os.getenv("APP_NAME", "EduForge AI")
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        
        # OpenAI Configuration
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        # Use real AI if API key provided, otherwise mock
        env_mock = os.getenv("USE_MOCK_AI", "").lower()
        self.use_mock_ai = env_mock == "true" or not self.openai_api_key
        
        # Supabase Configuration
        self.supabase_url = os.getenv("SUPABASE_URL", "")
        self.supabase_key = os.getenv("SUPABASE_KEY", "")
        
        # Server Configuration
        self.host = os.getenv("HOST", "0.0.0.0")
        self.port = int(os.getenv("PORT", "8000"))
        
        # CORS Configuration
        self.cors_origins = os.getenv(
            "CORS_ORIGINS",
            "http://localhost:3000,http://localhost:5173,https://*.vercel.app"
        ).split(",")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
