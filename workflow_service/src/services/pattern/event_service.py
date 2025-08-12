from src.redis.redis_service import ServiceRedis
from src.repositories.scenario_repo import ScenarioRepo
from src.services.scenario_service import ScenarioService

from src.logger import logger

from src.schemas.event_schema import Event

from sqlalchemy.ext.asyncio import AsyncSession


class EventService:
    def __init__(
            self,
            redis_service: ServiceRedis,
            scenario_repo: ScenarioRepo,
            scenario_service: ScenarioService
    ):
        self.redis_service = redis_service
        self.scenario_repo = scenario_repo
        self.scenario_service = scenario_service

    async def check_event(
            self,
            chat_id: int
    ):
        try:
            updates = await self.redis_service.get_last_updates(chat_id, limit=1)

            if not updates:
                logger.info(f"No updates found for chat: {chat_id}")
                return None

            return self._parse_update(updates[0])

        except Exception as e:
            logger.exception(f"Failed to check event for chat_id={chat_id}")
            return {"msg": "Internal error", "error": str(e)}

    @staticmethod
    def _parse_update(update: dict):
        try:
            event = list(update)[1]
            message = update.get("message") or update.get("edited_message") or {}
            chat_data = message.get("chat", {})
            chat_id = chat_data.get("id")

            if not chat_id:
                raise ValueError("chat_id is missing")

            event_type = EventService._detect_event_type(message, event)

            event_payload = Event(event_type=event_type, chat_id=chat_id)
            return event_payload.model_dump()

        except Exception as e:
            logger.warning(f"Invalid update format: {e}, update={update}")
            return {"msg": "Internal event", "error": str(e)}

    @staticmethod
    def _detect_event_type(message: dict, event: str) -> str:
        if "new_chat_member" in message:
            return "new_chat_member"
        elif "left_chat_member" in message:
            return "left_chat_member"

        return event

    async def is_event_matched(
            self,
            chat_id: int,
            session: AsyncSession
    ):
        """in params used dependency injection (DI)"""
        scenario_list = await self.scenario_service.get_scenarios(chat_id, session)
        event = await self.check_event(chat_id)

        if not event:
            return False

        incoming_event_type = event.get("event_type")
        if not incoming_event_type:
            return False

        for scenario in scenario_list:
            if scenario.get("event")["type"] == incoming_event_type:
                return True

        return False
