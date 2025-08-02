from src.repositories.scenario_repo import ScenarioRepo
from src.services.scenario_service import ScenarioService
from src.services.pattern.event_service import EventService
from src.services.redis_service import ServiceRedis

from sqlalchemy.ext.asyncio import AsyncSession

from src.logger import logger


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

        result = await self.event_service.is_event_matched(chat_id, session)
        text = await self.redis_service.get_last_messages(chat_id)

        if not text:
            logger.warning(f"No messages found in Redis for chat_id={chat_id}")
            return False

        last_message = text[0]

        conditions = await self.scenario_service.get_scenarios(chat_id, session)

        if result:
            for condition in conditions:
                if condition.get("conditions").get("params")["word"] in last_message.get("text"):
                    return True

        return False
