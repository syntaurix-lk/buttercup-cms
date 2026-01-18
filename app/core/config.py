"""
Configuration Management using Pydantic Settings
================================================

This module loads all configuration from environment variables (.env file).
All settings are validated at startup using Pydantic's type system.

Usage:
    from app.core.config import settings
    print(settings.DATABASE_URL)
"""

from functools import lru_cache
from typing import List, Literal
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    All configuration values MUST come from .env file - no hardcoding allowed.
    """
    
    # =========================================================================
    # Application Settings
    # =========================================================================
    APP_NAME: str = "Buttercup CMS"
    APP_ENV: Literal["dev", "staging", "prod"] = "dev"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # =========================================================================
    # Database Configuration
    # =========================================================================
    DATABASE_URL: str
    
    # DDL Auto Behavior (similar to Spring Boot's ddl-auto)
    # - create: Drop all tables and recreate (DANGEROUS - dev only)
    # - update: Run Alembic migrations to latest (recommended)
    # - none:   Do nothing on startup
    DB_DDL_AUTO: Literal["create", "update", "none"] = "update"
    
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    
    # =========================================================================
    # CORS Configuration
    # =========================================================================
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8080"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string to list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
    
    # =========================================================================
    # File Upload Configuration
    # =========================================================================
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_MB: int = 10
    ALLOWED_IMAGE_TYPES: str = "image/jpeg,image/png,image/gif,image/webp,image/svg+xml"
    STATIC_URL_PREFIX: str = "/static"
    
    @property
    def max_upload_bytes(self) -> int:
        """Convert MB to bytes for file size validation."""
        return self.MAX_UPLOAD_MB * 1024 * 1024
    
    @property
    def allowed_image_types_list(self) -> List[str]:
        """Parse allowed image types from comma-separated string."""
        return [t.strip() for t in self.ALLOWED_IMAGE_TYPES.split(",") if t.strip()]
    
    # =========================================================================
    # Logging Configuration
    # =========================================================================
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    LOG_FILE_PATH: str = "logs/app.log"
    LOG_FORMAT: Literal["json", "text"] = "json"
    LOG_MAX_BYTES: int = 10485760  # 10MB
    LOG_BACKUP_COUNT: int = 5
    
    # =========================================================================
    # API Configuration
    # =========================================================================
    API_V1_PREFIX: str = "/api/v1"
    REQUEST_TIMEOUT: int = 60

    # =========================================================================
    # Admin Authentication
    # =========================================================================
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "change_me"
    
    # =========================================================================
    # Pydantic Settings Configuration
    # =========================================================================
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"  # Ignore extra env vars not defined in model
    )
    
    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate that DATABASE_URL is properly formatted."""
        if not v.startswith(("mysql+pymysql://", "mysql://", "sqlite://")):
            raise ValueError("DATABASE_URL must be a valid MySQL or SQLite connection string")
        return v


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Uses lru_cache to ensure settings are loaded only once
    and reused across the application.
    """
    return Settings()


# Global settings instance for easy access
settings = get_settings()
