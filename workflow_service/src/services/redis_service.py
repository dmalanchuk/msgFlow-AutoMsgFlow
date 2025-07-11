from src.redis.client_redis import redis
import json


class ServiceRedis:

    @staticmethod
    async def save_message(chat_id: int, text: str):
        key = f"chat:{chat_id}:messages"
        message = json.dumps({"chat_id": chat_id, "text": text})
        await redis.rpush(key, message)

    @staticmethod
    async def get_messages(chat_id: int, limit: int = 10):
        key = f"chat:{chat_id}:messages"
        messages = await redis.lrange(key, -limit, -1)
        return [json.loads(m) for m in messages]
