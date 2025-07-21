from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    discord_webhook_url: str
    gemini_api_key: str
    redis_url: str

    class Config:
        env_file = ".env"


settings = Settings()
