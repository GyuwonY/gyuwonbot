from pydantic_settings import BaseSettings
from pydantic import ValidationError


class Settings(BaseSettings):
    DATABASE_URL: str
    DISCORD_WEBHOOK_URL: str
    GEMINI_API_KEY: str
    REDIS_URL: str
    GOOGLE_SERVICE_ACCOUNT_JSON: str
    CALENDAL_ID: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


try:
    settings = Settings()
except ValidationError as e:
    for error in e.errors():
        field_name = error["loc"][0].upper() if error["loc"] else "UNKNOWN_FIELD"
        print(f"- {field_name}: {error['msg']}")
    import sys

    sys.exit(1)
