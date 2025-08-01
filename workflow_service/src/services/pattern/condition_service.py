from src.repositories.scenario_repo import ScenarioRepo
from src.services.scenario_service import ScenarioService
from src.services.pattern.event_service import EventService
from src.services.redis_service import ServiceRedis

from sqlalchemy.ext.asyncio import AsyncSession


class ConditionService:
    def __init__(
            self,
            redis_service: ServiceRedis,
            event_service: EventService,
            scenario_repo: ScenarioRepo,
            scenario_service: ScenarioService,
    ):
        self.redis_service = redis_service
        self.event_service = event_service
        self.scenario_repo = scenario_repo
        self.scenario_service = scenario_service

    async def check_conditions(
            self,
            chat_id: int,
            session: AsyncSession
    ) -> bool:
        """in params used dependency injection"""

        conditions = await self.scenario_service.get_scenarios(chat_id, session)
        result = await self.event_service.is_event_matched(chat_id, session)
        text = await self.redis_service.get_last_messages(chat_id)

        last_message = text[0]

        if result:
            for condition in conditions:
                if condition.conditions["params"].get("word") in last_message.get("text"):
                    return True

        return False
