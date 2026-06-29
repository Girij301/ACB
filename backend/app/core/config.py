from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


# ✅ OUTSIDE class (IMPORTANT FIX)
BASE_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    GEMINI_API_KEY: str
    MODEL_NAME: str = "gemini-2.5-flash"

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    ALLOWED_ORIGINS: str = "http://localhost:3000"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore"
    )


settings = Settings()