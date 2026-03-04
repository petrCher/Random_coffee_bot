from pydantic import ConfigDict, PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    BOT_TOKEN: str
    #DB_DSN: PostgresDsn
    # MARKETING_URL: str //future tasks

    model_config = ConfigDict(case_sensitive=True, env_file=".env", extra="allow")
