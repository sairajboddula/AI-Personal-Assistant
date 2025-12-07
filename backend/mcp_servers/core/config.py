from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """MCP Server Configuration"""
    
    # Server Settings
    PROJECT_NAME: str = "MCP Server"
    API_V1_STR: str = "/api/v1"
    PORT: int = 8000
    DEBUG: bool = True
    
    # =============================================================================
    # ZOMATO INTEGRATION
    # =============================================================================
    ZOMATO_API_KEY: str = "mock-zomato-key"
    ZOMATO_API_URL: str = "https://developers.zomato.com/api/v2.1"
    ZOMATO_MOCK_MODE: bool = True
    
    # =============================================================================
    # AMAZON INTEGRATION
    # =============================================================================
    AMAZON_API_KEY: str = "mock-amazon-key"
    AMAZON_SECRET_KEY: Optional[str] = None
    AMAZON_API_URL: str = "https://webservices.amazon.com/paapi5"
    AMAZON_MOCK_MODE: bool = True
    
    # =============================================================================
    # BANKING INTEGRATION
    # =============================================================================
    BANK_API_KEY: str = "mock-bank-key"
    BANK_API_URL: str = "https://api.yourbank.com/v1"
    BANK_ACCOUNT_ID: str = "default-account"
    BANK_MOCK_MODE: bool = True
    
    # =============================================================================
    # ADDITIONAL INTEGRATIONS (Optional)
    # =============================================================================
    OPENAI_API_KEY: Optional[str] = None
    GOOGLE_CALENDAR_API_KEY: Optional[str] = None
    SPOTIFY_CLIENT_ID: Optional[str] = None
    SPOTIFY_CLIENT_SECRET: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Allow extra fields from .env without validation errors

settings = Settings()

