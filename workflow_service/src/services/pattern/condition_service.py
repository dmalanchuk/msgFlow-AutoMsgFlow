from src.repositories.scenario_repo import ScenarioRepo
from src.services.pattern.event_service import EventService
from src.services.redis_service import ServiceRedis

from sqlalchemy.ext.asyncio import AsyncSession


class ConditionService:

    @staticmethod
    async def check_conditions(
            chat_id: int,
            redis_service: ServiceRedis,
            event_service: EventService,
            session: AsyncSession
    ) -> bool:
        """in params used dependency injection"""

        conditions = await ScenarioRepo.get_scenario(chat_id, session)
        result = await event_service.is_event_matched(chat_id, session)
        text = await redis_service.get_last_messages(chat_id)

        last_message = text[0]

        if result:
            for condition in conditions:
                if condition.conditions["params"].get("word") in last_message.get("text"):
                    return True

        return False


