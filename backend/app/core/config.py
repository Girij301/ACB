from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[3]
WORKSPACE_DIR = BASE_DIR / "workspace" 

WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    MODEL_NAME: str = "gemini-2.5-flash"
    WORKSPACE_DIR: Path = BASE_DIR / "workspace"
    MEMORY_LIMIT: int = 20
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    ALLOWED_ORIGINS: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")


settings = Settings()

settings.WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
