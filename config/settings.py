from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from .env file and environment variables.
    """
    LLM_BASE_URL: Optional[str] = "https://api.openai.com/v1"
    LLM_API_KEY: str
    LLM_TIMEOUT: Optional[int] = 15 # Default to 60 seconds

    NOTION_TOKEN: str
    NOTION_DATABASE_ID: str
    TEST_NOTION_DATABASE_ID: str

    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_CHAT_ID: str

    PROXY_URL: Optional[str] = None

    LOG_LEVEL: str = "DEBUG"

    TOP_N_NEWS: int = 10
    TOP_M_COMMENTS: int = 5

    TEST_MODE: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()