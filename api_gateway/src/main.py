from fastapi import FastAPI
from src.api import routes
from src.config import settings
from src.utils.auth_middleware import AuthMiddleware
app = FastAPI(
    title=settings.SERVICE_NAME
)

app.add_middleware(AuthMiddleware)

app.include_router(routes.router, tags=["routes"])
