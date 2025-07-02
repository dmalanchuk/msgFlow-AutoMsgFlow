from fastapi import APIRouter
from src.connections.telegram import telegram_integration

router = APIRouter()
router.include_router(telegram_integration.router, prefix="/webhook", tags=["Telegram"])
