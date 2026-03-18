import os
from functools import lru_cache

from pydantic import ConfigDict, PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    BOT_TOKEN: str
    DB_DSN: str
    # MARKETING_URL: str //future tasks

    model_config = ConfigDict(case_sensitive=True, env_file=".env", extra="allow")

@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
