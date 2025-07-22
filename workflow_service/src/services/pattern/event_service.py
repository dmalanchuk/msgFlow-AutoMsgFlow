from sqlalchemy.ext.asyncio import AsyncSession

from src.services.redis_service import ServiceRedis


class EventService:

    @staticmethod
    async def check_event(event_type: str, session: AsyncSession):
        ...
