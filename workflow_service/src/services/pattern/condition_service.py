from pydantic import json

from src.repositories.scenario_repo import ScenarioRepo
from src.services.scenario_service import ScenarioService
from src.services.pattern.event_service import EventService
from src.redis.redis_service import ServiceRedis

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

        if not result:
            logger.info(f"Event not matched for chat_id={chat_id}")
            return False

        text = await self.redis_service.get_last_messages(chat_id)

        if not text:
            logger.warning(f"No messages found in Redis for chat_id={chat_id}")
            return False
        last_message = text[0]

        conditions = await self.scenario_service.get_scenarios(chat_id, session)

        if result and last_message.get("text"):
            for condition in conditions:
                conditions_dict = condition.get("conditions") or {}
                params = conditions_dict.get("params") or {}
                word = params.get("word")

                if word and word in last_message["text"]:
                    return True

        return False

    async def check_conditions_for_scenario(self, scenario, chat_id: int, message_id, session):
        # Get last message in Redis
        messages = await self.redis_service.get_message_by_id(chat_id, message_id)
        if not messages:
            logger.warning(f"No message in Redis for chat_id={chat_id}", message_id = {message_id})
            return False

        last_message = messages.get("text", "")
        logger.info(f"Message {message_id} from Redis: {last_message}")

        # Get condition raw
        condition_raw = scenario.conditions
        logger.info(f"Condition raw: {condition_raw}")

        if isinstance(condition_raw, str):
            try:
                condition = json.loads(condition_raw)
            except json.JSONDecodeError:
                logger.error("Error parsing JSON в scenario.conditions")
                return False
        else:
            condition = condition_raw

        condition_type = condition.get("type")
        condition_params = condition.get("params", {})

        # 3. Data type processing
        if condition_type == "contains_word":
            word = condition_params.get("word", "").lower()
            if word in last_message.lower():
                logger.info(f"Match by contains_word: '{word}' found in '{last_message}'")
                return True
            else:
                logger.info(f"Word '{word}' not found in '{last_message}'")

        return False