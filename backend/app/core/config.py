from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """central configuration settings for the application
    all settings are loaded from environment variables
    """

    APP_NAME: str = "Synapse AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    HOST: str
    PORT: int

    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432

    JWT_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )

@lru_cache()
def get_settings() -> Settings:
    """get the settings from the environment variables
    and cache them for future use.
    Creates only ONE Settings object.
    """
    return Settings()

settings = get_settings()