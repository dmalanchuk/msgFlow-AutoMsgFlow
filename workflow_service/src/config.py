from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    TELEGRAM_TOKEN: str

    RABBITMQ_URL: str
    QUEUE_NAME: str

    class Config:
        env_file = ".env"


settings = Settings()
