from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "Gumroad AI Empire"
    version: str = "1.0.0"
    debug: bool = True

    database_url: str = "sqlite+aiosqlite:///./gumroad_ai.db"
    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/1"
    use_database: bool = True

    secret_key: str = "super-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o"

    groq_api_key: Optional[str] = None
    groq_model: str = "llama-3.3-70b-versatile"

    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2:latest"

    ai_provider: str = "auto"  # auto, openai, groq, ollama

    gumroad_api_key: Optional[str] = None
    gumroad_client_id: Optional[str] = None
    gumroad_client_secret: Optional[str] = None

    twitter_api_key: Optional[str] = None
    twitter_api_secret: Optional[str] = None
    twitter_bearer_token: Optional[str] = None

    linkedin_client_id: Optional[str] = None
    linkedin_client_secret: Optional[str] = None

    mailgun_api_key: Optional[str] = None
    mailgun_domain: Optional[str] = None
    from_email: str = "noreply@gumroad.ai"

    sentry_dsn: Optional[str] = None

    max_agents_concurrency: int = 5
    agent_timeout_seconds: int = 120

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
