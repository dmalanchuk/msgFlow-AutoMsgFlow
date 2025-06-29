from pydantic import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str = "API Gateway"


settings = Settings()
