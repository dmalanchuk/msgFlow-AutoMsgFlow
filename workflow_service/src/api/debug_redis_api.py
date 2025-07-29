from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.redis_service import ServiceRedis
from src.services.pattern.event_service import EventService
from src.services.pattern.condition_service import ConditionService
from src.database import get_session

router_debug = APIRouter(prefix="/debug")


@router_debug.get("/chat/{chat_id}/messages")
async def get_chat_messages(chat_id: int, limit: int = 10):
    return await ServiceRedis.get_last_messages(chat_id, limit)


@router_debug.get("/chat/{chat_id}/updates")
async def get_chat_updates(chat_id: int, limit: int = 10):
    return await ServiceRedis.get_last_updates(chat_id, limit)


@router_debug.get("/chat/{chat_id}/event")
async def get_chat_event(chat_id: int):
    return await EventService.check_event(chat_id)


@router_debug.get("/chat/{chat_id}/event/matched")
async def is_event_matched(chat_id: int, session: AsyncSession = Depends(get_session)):
    return await ConditionService.is_event_matched(chat_id, session)


@router_debug.get("/chat/{chat_id}/conditions")
async def check_conditions(chat_id: int, session: AsyncSession = Depends(get_session)):
    return await ConditionService.check_conditions(chat_id, session)
