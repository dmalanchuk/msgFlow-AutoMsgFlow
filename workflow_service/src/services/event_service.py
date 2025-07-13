from src.schemas.event_schema import Event
from src.repositories.event_repo import EventRepo

from sqlalchemy.ext.asyncio import AsyncSession


class EventService:

    @staticmethod
    async def check_event(data: Event, session: AsyncSession):
        scenarios = await EventRepo.get_event(data, session)

        if not scenarios:
            return {"msg": "no scenario with this event"}
