from typing import Any, Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables and/or a .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # General
    ENV: Literal["development", "testing", "staging", "production"] = "development"
    DEBUG: bool = False
    APP_TITLE: str = "FastAPI Base Service"
    APP_VERSION: str = "0.1.0"

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Logging
    LOG_FILE: str | None = "logs/app.log"
    LOG_LEVEL: str = "INFO"
    LOG_ROTATION: Literal["size", "time"] = "size"
    LOG_MAX_BYTES: int = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT: int = 5

    # CORS Settings
    ALLOWED_ORIGINS: list[str] = ["*"]

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_allowed_origins(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        if isinstance(v, list):
            return [str(origin).strip() for origin in v]
        return []


# Global configuration instance
settings = Settings()
