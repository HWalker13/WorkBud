from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Core
    database_url: str = "postgresql://user:password@localhost:5432/gymbuddy"

    # JWT
    secret_key: str = "change-me-to-a-long-random-string"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 10080  # 7 days

    # CORS
    frontend_url: str = "http://localhost:5173"

    # Phase 2: S3
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_s3_bucket: str = "gymbuddy-photos"
    aws_region: str = "us-east-1"

    # Phase 2: AI
    openai_api_key: str = ""

    # Phase 6: Celery / Redis
    redis_url: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
