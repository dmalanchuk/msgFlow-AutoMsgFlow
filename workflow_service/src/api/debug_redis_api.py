from fastapi import Depends
from src.database import get_session
from fastapi import APIRouter
from src.services.redis_service import ServiceRedis
from src.services.pattern.event_service import EventService
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.condition_action_schema import ConditionAction

router_debug = APIRouter(prefix="/debug")


@router_debug.get("/chat/{chat_id}/messages")
async def get_chat_messages(chat_id: int, limit: int = 10):
    return await ServiceRedis.get_last_messages(chat_id, limit)


@router_debug.get("/chat/{chat_id}/updates")
async def get_chat_updates(chat_id: int, limit: int = 10):
    return await ServiceRedis.get_last_updates(chat_id, limit)


@router_debug.get("/chat/{chat_id}/event")
async def get_chat_event(chat_id: int,
                         data: ConditionAction,
                         session: AsyncSession = Depends(get_session)
                         ):
    return await EventService.check_event(chat_id, data, session)
