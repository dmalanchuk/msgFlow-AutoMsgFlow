from src.repositories.scenario_repo import ScenarioRepo
from src.services.pattern.event_service import EventService

from sqlalchemy.ext.asyncio import AsyncSession


class ConditionService:

    @staticmethod
    async def is_event_matched(chat_id: int, session: AsyncSession) -> bool:
        result = await ScenarioRepo.get_scenario(chat_id, session)
        event = await EventService.check_event(chat_id)

        if not event:
            return False

        incoming_event_type = event.get("event_type")
        if not incoming_event_type:
            return False

        for scenario in result:
            if scenario.event["type"] == incoming_event_type:
                return True

        return False

    @staticmethod
    async def check_conditions(chat_id: int, session: AsyncSession) -> bool:
        ...
