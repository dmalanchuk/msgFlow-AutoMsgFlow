from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.redis_service import ServiceRedis
from src.services.pattern.action_service import ActionService
from src.database import get_session

from src.dependency import condition_service, event_service

router_debug = APIRouter(prefix="/debug")


@router_debug.get("/chat/{chat_id}/messages")
async def get_chat_messages(chat_id: int, limit: int = 10):
    return await ServiceRedis.get_last_messages(chat_id, limit)


@router_debug.get("/chat/{chat_id}/updates")
async def get_chat_updates(chat_id: int, limit: int = 10):
    return await ServiceRedis.get_last_updates(chat_id, limit)


@router_debug.get("/chat/{chat_id}/event")
async def get_chat_event(chat_id: int):
    return await event_service.check_event(chat_id)


@router_debug.get("/chat/{chat_id}/event/matched")
async def is_event_matched(chat_id: int, session: AsyncSession = Depends(get_session)):
    return await event_service.is_event_matched(chat_id, session)


@router_debug.get("/chat/{chat_id}/conditions")
async def check_conditions(chat_id: int, session: AsyncSession = Depends(get_session)):
    return await condition_service.check_conditions(chat_id, session)


@router_debug.get("/chat/{chat_id}/actions")
async def send_actions(chat_id: int, session: AsyncSession = Depends(get_session)):
    return await ActionService.send_action_from_scenario(chat_id, session)
