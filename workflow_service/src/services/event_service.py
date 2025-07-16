from src.schemas.condition_action_schema import ConditionAction
from src.schemas.event_schema import Event

from src.repositories.event_repo import EventRepo
from src.services.condition_service import ConditionService
from src.services.action_service import ActionService

from sqlalchemy.ext.asyncio import AsyncSession


class EventService:

    @staticmethod
    async def check_event(data: Event, session: AsyncSession):
        ...
