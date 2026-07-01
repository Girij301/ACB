from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[3]
WORKSPACE_DIR = BASE_DIR / "workspace"

WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)


class Settings(BaseSettings):
    # AI Configuration
    GEMINI_API_KEY: str
    MODEL_NAME: str = "gemini-2.5-flash"

    # Workspace
    WORKSPACE_DIR: Path = BASE_DIR / "workspace"

    # Memory
    MEMORY_LIMIT: int = 20

    # Retry Configuration
    MAX_RETRIES: int = 3
    MAX_AI_FIX_ATTEMPTS: int = 3

    # Validation
    ENABLE_VALIDATION: bool = True

    DEFAULT_VALIDATORS: tuple[str, ...] = (
        "python -m compileall .",
        "ruff check .",
    )

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Debugging
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )


settings = Settings()

settings.WORKSPACE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)
