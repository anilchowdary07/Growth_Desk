from __future__ import annotations

"""Core configuration module for AI GrowthDesk."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""

    # App
    APP_NAME: str = "AI GrowthDesk"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = "growthdesk-dev-secret-key-32-bytes-long!!"  # For JWT signing
    ENCRYPTION_KEY: str = "GDYPbCUrkW2NY8ikqDSyr2dNcgDKUb2AQLzHrQiQFd4="  # For Fernet encryption of API keys

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/growthdesk"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    JWT_ALGORITHM: str = "HS256"

    # S3-compatible storage
    S3_ENDPOINT: str = ""
    S3_BUCKET: str = "growthdesk"
    S3_ACCESS_KEY: str = ""
    S3_SECRET_KEY: str = ""
    S3_REGION: str = "us-east-1"

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # Frontend URL (for CORS)
    FRONTEND_URL: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings instance."""
    return Settings()
