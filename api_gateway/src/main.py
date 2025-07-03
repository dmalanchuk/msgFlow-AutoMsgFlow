from fastapi import FastAPI
from api_gateway.src.api import routes
from api_gateway.src.config import settings

app = FastAPI(
    title=settings.SERVICE_NAME
)

app.include_router(routes.router, tags=["routes"])
