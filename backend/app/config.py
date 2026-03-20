from pydantic_settings import BaseSettings
from typing import Optional
import os
from functools import lru_cache


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-Adaptive Onboarding Engine"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./ai_onboarding.db"
    )
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # AI/ML Settings
    SENTENCE_TRANSFORMER_MODEL: str = "all-MiniLM-L6-v2"
    SPACY_MODEL: str = "en_core_web_sm"
    
    # Google AI
    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
    
    # File Upload
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Skills Database
    SKILLS_TAXONOMY_PATH: str = "./data/skills/taxonomy.json"
    COURSE_CATALOG_PATH: str = "./data/courses/catalog.json"
    
    # Priority Engine Weights
    GAP_WEIGHT: float = 0.4
    IMPORTANCE_WEIGHT: float = 0.35
    DEPENDENCY_WEIGHT: float = 0.25
    
    # Adaptive Engine
    LEARNING_GAIN_RATE: float = 0.8
    PROGRESS_THRESHOLD: float = 0.15
    ROADMAP_RECOMPUTE_TRIGGER: float = 0.2
    
    # CORS
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:5174")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
