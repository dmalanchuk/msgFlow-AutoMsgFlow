from fastapi import APIRouter
from src.services.redis_service import ServiceRedis

router_debug = APIRouter(prefix="/debug")


@router_debug.get("/chat/{chat_id}")
async def get_chat_messages(chat_id: int):
    return await ServiceRedis.get_last_messages(chat_id)
