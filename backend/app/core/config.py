from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[3]
WORKSPACE_DIR = BASE_DIR / "workspace"

WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)


class Settings(BaseSettings):
    """
    Global application configuration.
    """

    # AI
    GEMINI_API_KEY: str
    MODEL_NAME: str = "gemini-2.5-flash"

    # Docker
    DOCKER_ENABLED: bool = True
    DOCKER_IMAGE: str = "python:3.12-slim"
    DOCKER_CONTAINER_PREFIX: str = "acb-agent"
    DOCKER_WORKDIR: str = "/workspace"
    DOCKER_NETWORK_DISABLED: bool = True
    DOCKER_AUTO_REMOVE: bool = False
    DOCKER_MEMORY_LIMIT: str = "512m"
    DOCKER_NANO_CPUS: int = 1_000_000_000

    # Memory
    MEMORY_LIMIT: int = 20

    # Retry
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

    # Logging
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )


settings = Settings()
