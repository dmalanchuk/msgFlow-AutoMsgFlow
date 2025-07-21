from src.redis.client_redis import redis
import json


class ServiceRedis:

    @staticmethod
    async def save_update(chat_id: int, update: dict):
        key = f"chat:{chat_id}:updates"
        await redis.rpush(key, json.dumps(update))
        await redis.expire(key, 86400)  # 1 день

    @staticmethod
    async def save_message(chat_id: int, text: str):
        key = f"chat:{chat_id}:messages"
        await redis.rpush(key, json.dumps({"text": text}))
        await redis.expire(key, 86400)  # 1 день

    @staticmethod
    async def get_last_messages(chat_id: int, limit: int = 1):
        key = f"chat:{chat_id}:messages"
        messages = await redis.lrange(key, -limit, -1)
        return [json.loads(m) for m in messages]

    @staticmethod
    async def get_last_updates(chat_id: int, limit: int = 10):
        key = f"chat:{chat_id}:updates"
        updates = await redis.lrange(key, -limit, -1)
        return [json.loads(update) for update in updates]
