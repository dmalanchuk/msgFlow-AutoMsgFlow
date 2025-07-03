from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings: name, host, port"""
    SERVICE_NAME: str = "API Gateway"
    SERVICE_HOST: str = "0.0.0.0"
    SERVICE_PORT: int = 8000

    """All url for services"""
    AUTH_SERVICE_URL: str = "http://auth_service:8000"
    INTERACTION_SERVICE_URL: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
