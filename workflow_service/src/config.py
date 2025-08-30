from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    TEST_DATABASE_URL: str
    TELEGRAM_TOKEN: str

    RABBITMQ_URL: str
    QUEUE_NAME: str
    ACTION_QUEUE_NAME: str

    REDIS_URL: str

    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = ".env"


settings = Settings()
