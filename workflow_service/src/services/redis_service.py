from src.redis.client_redis import redis
from src.decorators import timer
import json


class ServiceRedis:
    """saved last updates and messages"""

    @staticmethod
    @timer
    async def save_update(chat_id: int, update: dict):
        key = f"chat:{chat_id}:updates"
        await redis.rpush(key, json.dumps({
            "event_type": list(update)[1]
        }))
        await redis.expire(key, 500)  # 86400

    @staticmethod
    @timer
    async def save_message(chat_id: int, text: str, msg_id: int, source: str, event_type: str):
        key = f"chat:{chat_id}:messages"
        await redis.rpush(key, json.dumps(
            {
                "source": source,
                "event_type": event_type,
                "text": text,
                "message_id": msg_id
            }
        ))
        await redis.expire(key, 500)  # 86400

    """get last updates and messages"""

    @staticmethod
    async def get_last_messages(chat_id: int, limit: int = 1):
        key = f"chat:{chat_id}:messages"
        messages = await redis.lrange(key, -limit, -1)
        return [json.loads(m) for m in messages]

    @staticmethod
    async def get_last_updates(chat_id: int, limit: int = 1):
        key = f"chat:{chat_id}:updates"
        updates = await redis.lrange(key, -limit, -1)
        return [json.loads(update) for update in updates]
