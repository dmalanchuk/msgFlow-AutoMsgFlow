from src.services.redis_service import ServiceRedis
from src.repositories.scenario_repo import ScenarioRepo
from src.logger import logger

from src.schemas.event_schema import Event

from sqlalchemy.ext.asyncio import AsyncSession


class EventService:

    @staticmethod
    async def check_event(
            chat_id: int,
            redis_service: ServiceRedis
    ):
        try:
            updates = await redis_service.get_last_updates(chat_id, limit=1)

            if not updates:
                logger.info(f"No updates found for chat: {chat_id}")
                return {"msg": "No updates"}

            return EventService._parse_update(updates[0])

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
        try:
            if "new_chat_member" in message:
                return "new_chat_member"
            elif "left_chat_member" in message:
                return "left_chat_member"

            return event
        except Exception as e:
            logger.warning(f"Failed to detect event type: {e}, message={message}, event={event}")
            return "unknown"

    @staticmethod
    async def is_event_matched(
            chat_id: int,
            redis_service: ServiceRedis,
            scenario_repo: ScenarioRepo,
            session: AsyncSession
    ):
        """in params used dependency injection (DI)"""
        try:

            scenario_list = await scenario_repo.get_scenario(chat_id, session)
            event = await EventService.check_event(chat_id, redis_service)

            if not event:
                return False

            incoming_event_type = event.get("event_type")
            if not incoming_event_type:
                return False

            for scenario in scenario_list:
                if scenario.event["type"] == incoming_event_type:
                    return True

            return False

        except Exception as e:
            logger.exception(f"Failed to check event for chat_id={chat_id}, error: {e}")
            return False
