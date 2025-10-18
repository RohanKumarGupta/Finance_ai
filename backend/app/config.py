from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path

class Settings(BaseSettings):
    MONGODB_URI: str = Field(..., description="MongoDB connection string")
    DATABASE_NAME: str = "finance_db"
    JWT_SECRET: str = Field(...)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    GEMINI_API_KEY: str | None = None

    class Config:
        # Ensure we load backend/.env even when running from project root
        env_file = str((Path(__file__).resolve().parents[1] / ".env"))
        extra = "ignore"

settings = Settings()
