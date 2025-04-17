from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):

    APP_NAME: str = "Default App Name"
    APP_VERSION: str = "0.0.1"
    DEBUG_MODE: bool = False

    JWT_SECRET_KEY: str = "default"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    DATABASE_PASSWORD: str = ""

    DATABASE_URL: str = ""

    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_USER: str = "user"
    DATABASE_NAME: str = "postgresDB"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_URL: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(
        env_file= Path(__file__).resolve().parents[2] / ".env",
        env_file_encoding='utf-8',
        extra='ignore'
    )

@lru_cache
def get_settings() -> Settings:
    print("Loading application settings...")
    return Settings()

settings = get_settings()
# print(settings.APP_NAME)
