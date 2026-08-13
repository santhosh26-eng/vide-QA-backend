from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = Path(__file__).resolve().parent.parent.parent / ".env"


class Settings(BaseSettings):
    mistral_api_key: str
    gemini_api_key: str

    mongodb_url: str
    database_name: str

    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH) if ENV_PATH.exists() else ".env",
        extra="ignore",
        case_sensitive=False
    )


settings = Settings()