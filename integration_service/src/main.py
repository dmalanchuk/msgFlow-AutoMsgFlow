from fastapi import FastAPI
from src.connections.telegram.telegram_integration import router as telegram_router

app = FastAPI()
app.include_router(telegram_router, tags=["telegram"])
