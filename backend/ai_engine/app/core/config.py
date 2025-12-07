from pydantic_settings import BaseSettings
from typing import Optional, List

class Settings(BaseSettings):
    """AI Engine Configuration"""
    
    # Server Settings
    PROJECT_NAME: str = "AI Engine"
    PORT: int = 8001
    DEBUG: bool = True
    
    # MCP Server Connection
    MCP_SERVER_URL: str = "http://localhost:8000/api/v1"
    
    # AI Model Configuration
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_TEMPERATURE: float = 0.7
    OPENAI_MAX_TOKENS: int = 500
    
    # Alternative AI Providers
    ANTHROPIC_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    
    # CORS Settings
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Allow extra fields from .env without validation errors

settings = Settings()

