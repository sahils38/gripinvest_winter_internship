from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=False
    )

    database_url: str = Field(alias="DATABASE_URL")
    jwt_secret: str = Field(default="changeme", alias="JWT_SECRET")

@lru_cache
def get_settings() -> Settings:
    return Settings()
