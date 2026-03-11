# PHASE 1 COMPLIANCE: This file MUST NOT import or call any LLM API.
# Forbidden: openai, anthropic, langchain, llama_index, cohere, groq
# This is a Zero-Backend-LLM architecture. Violation = disqualification.

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Application Configuration
    APP_ENV: str = "development"
    SECRET_KEY: str
    API_KEY_HEADER: str = "X-API-Key"

    # Database Configuration
    DATABASE_URL: str

    # Cloudflare R2 Configuration (optional - for cloud deployment)
    R2_ENDPOINT_URL: str = ""
    R2_ACCESS_KEY_ID: str = ""
    R2_SECRET_ACCESS_KEY: str = ""
    R2_BUCKET_NAME: str = ""

    # CORS Configuration
    CHATGPT_APP_ORIGIN: str = "https://chat.openai.com"

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Freemium Configuration
    FREE_TIER_MAX_CHAPTERS: int = 3

    # Storage Configuration (local or r2)
    STORAGE_TYPE: str = "local"
    LOCAL_CONTENT_PATH: str = "./content"

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.APP_ENV == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.APP_ENV == "production"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance.
    
    Returns:
        Settings: Application settings instance.
    """
    return Settings()
