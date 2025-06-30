from fastapi import FastAPI
from integration_service.src.connectors.telegram.telegram_conn import router as telegram_router

app = FastAPI()
app.include_router(telegram_router, tags=["telegram"])
