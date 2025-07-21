from src.redis.client_redis import redis
import json


class ServiceRedis:

    # @staticmethod
    # async def save_update(chat_id: int, update: dict):
    #     key = f"chat:{chat_id}:updates"
    #     await redis.rpush(key, json.dumps(update))
    #     await redis.expire(key, 86400)

    # @staticmethod
    # async def get_last_messages(chat_id: int, limit: int = 1):
    #     key = f"chat:{chat_id}:messages"
    #     messages = await redis.lrange(key, -limit, -1)
    #     return [json.loads(m) for m in messages]

    @staticmethod
    async def save_update(chat_id: int, update: dict):
        update_type = ServiceRedis.get_update_type(update)

        key_updates = f"chat:{chat_id}:updates"
        await redis.rpush(key_updates, json.dumps(update))
        await redis.expire(key_updates, 86400)

        if update_type == "message" and "text" in update["message"]:
            key_messages = f"chat:{chat_id}:messages"
            await redis.rpush(key_messages, json.dumps(update["message"]))
            await redis.expire(key_messages, 86400)

        if update_type == "message" and "new_chat_members" in update["message"]:
            key_joins = f"chat:{chat_id}:joins"
            for member in update["message"]["new_chat_members"]:
                await redis.rpush(key_joins, json.dumps(member))
            await redis.expire(key_joins, 86400)

    @staticmethod
    async def get_last_messages(chat_id: int, limit: int = 1):
        key = f"chat:{chat_id}:messages"
        messages = await redis.lrange(key, -limit, -1)
        return [json.loads(m) for m in messages]

    @staticmethod
    def get_update_type(update: dict) -> str:
        for key in [
            "message",
            "edited_message",
            "channel_post",
            "edited_channel_post",
            "inline_query",
            "chosen_inline_result",
            "callback_query",
            "shipping_query",
            "pre_checkout_query",
            "poll",
            "poll_answer",
            "my_chat_member",
            "chat_member",
            "chat_join_request"
        ]:
            if key in update:
                return key
        return "unknown"
