from pydantic_settings import BaseSettings
import os
from pathlib import Path

# Load .env file before creating settings
env_file_path = None
backend_dir = Path(__file__).parent.parent.parent
if (backend_dir / ".env").exists():
    env_file_path = backend_dir / ".env"
elif (backend_dir / "app" / ".env").exists():
    env_file_path = backend_dir / "app" / ".env"

# Load env vars from file if it exists
if env_file_path:
    from dotenv import load_dotenv
    load_dotenv(str(env_file_path))

class Settings(BaseSettings):
    APP_NAME: str = "Girls in Science"
    SECRET_KEY: str = "super-tajna-sifra-promijeni-me-kasneje"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "sqlite:///./sql_app.db"

    class Config:
        case_sensitive = False

settings = Settings()