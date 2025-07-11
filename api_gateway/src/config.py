from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings: name, host, port"""
    SERVICE_NAME: str = "API Gateway"
    SERVICE_HOST: str = "0.0.0.0"
    SERVICE_PORT: int = 8000

    """All url for services"""
    # AUTH_SERVICE_URL: str = "http://auth_service:8000"
    AUTH_SERVICE_URL: str = "http://127.0.0.1:8000"
    INTERACTION_SERVICE_URL: str = ""

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    class Config:
        env_file = ".env"


settings = Settings()
