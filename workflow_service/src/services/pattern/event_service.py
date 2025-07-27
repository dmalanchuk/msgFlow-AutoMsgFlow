from src.services.redis_service import ServiceRedis
from src.decorators import timer


class EventService:

    @staticmethod
    @timer
    async def check_event(chat_id: int):
        updates = await ServiceRedis.get_last_updates(chat_id, limit=1)

        if not updates:
            return {"msg": "No updates"}

        last_update = updates[0]
        event_type = list(last_update)[1]
        message_data = last_update.get("message") or last_update.get("edited_message")
        chat_id = message_data.get(
            "chat", {}).get(
            "id", ""
        )

        if "new_chat_member" in message_data:
            event_type = "new_chat_member"
        elif "left_chat_member" in message_data:
            event_type = "left_chat_member"
        elif "photo" in message_data:
            event_type = "photo"

        event_payload = {
            "event_type": event_type,
            "chat_id": chat_id
        }

        return event_payload
