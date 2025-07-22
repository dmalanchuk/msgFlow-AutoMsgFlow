from src.services.redis_service import ServiceRedis


class EventService:

    @staticmethod
    async def check_event(chat_id: int):
        updates = await ServiceRedis.get_last_messages(chat_id, limit=1)

        if not updates:
            return {"msg": "No updates"}

        last_update = updates[0]
        source = last_update["source"]
        event_type = last_update["event_type"]

        event_payload = {
            "source": source,
            "event_type": event_type
        }

        return event_payload
