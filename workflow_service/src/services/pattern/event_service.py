from src.services.redis_service import ServiceRedis
from src.logger import logger

from src.schemas.event_schema import Event


class EventService:

    @staticmethod
    async def check_event(chat_id: int) -> dict:
        try:
            updates = await ServiceRedis.get_last_updates(chat_id, limit=1)

            if not updates:
                logger.info(f"No updates found for chat: {chat_id}")
                return {"msg": "No updates"}

            return EventService._parse_update(updates[0])

        except Exception as e:
            logger.exception(f"Failed to check event for chat_id={chat_id}")
            return {"msg": "Internal error", "error": str(e)}

    @staticmethod
    def _parse_update(update: dict) -> dict:
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
                event = "new_chat_member"
            elif "left_chat_member" in message:
                event = "left_chat_member"

            return event
        except Exception as e:
            logger.warning(f"Failed to detect event type: {e}, message={message}, event={event}")
            return "unknown"
