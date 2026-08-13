from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = 'AI Career Agent'
    app_version: str = '0.1.0'
    environment: str = 'development'
    database_url: str = 'postgresql://user:pass@localhost:5432/career_agent'
    redis_url: str = 'redis://localhost:6379/0'
    jwt_secret: str = 'change-me'
    jwt_expiry_minutes: int = 60
    llm_api_key: str = ''
    llm_model: str = 'gpt-4o-mini'
    embedding_model: str = 'text-embedding-3-small'
    object_storage_bucket: str = 'career-agent-storage'
    object_storage_key: str = ''
    object_storage_secret: str = ''

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
