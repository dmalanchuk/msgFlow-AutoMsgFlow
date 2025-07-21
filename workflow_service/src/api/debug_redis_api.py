from fastapi import APIRouter
from src.services.redis_service import ServiceRedis

router_debug = APIRouter(prefix="/debug")


@router_debug.get("/chat/{chat_id}/messages")
async def get_chat_messages(chat_id: int, limit: int = 10):
    """Отримати останні текстові повідомлення."""
    return await ServiceRedis.get_last_messages(chat_id, limit)


@router_debug.get("/chat/{chat_id}/updates")
async def get_chat_updates(chat_id: int, limit: int = 10):
    """Отримати останні повні Telegram update-и."""
    return await ServiceRedis.get_last_updates(chat_id, limit)
