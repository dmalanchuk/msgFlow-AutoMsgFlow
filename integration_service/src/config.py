from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TELEGRAM_TOKEN: str
    RABBITMQ_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
