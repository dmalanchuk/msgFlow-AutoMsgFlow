import json
from pydantic import EmailStr

from src.redis.client_redis import redis
from src.schemas.event_redis_schema import SaveUpdate
from src.schemas.actions_redis_schema import ActionsRedis
from src.utils.make_safe_mail import make_chat_key


# saved last updates and messages
async def save_update(chat_id: int, update: SaveUpdate):
    key = f"chat:{chat_id}:updates"
    await redis.rpush(key, update.model_dump_json())
    await redis.expire(key, 500)  # 86400


# async def save_message(chat_id: int, text: str, msg_id: int, source: str, event_type: str):
#     key = f"chat:{chat_id}:messages"
#     await redis.rpush(key, json.dumps(
#         {
#             "source": source,
#             "event_type": event_type,
#             "text": text,
#             "message_id": msg_id
#         }
#     ))
#     await redis.expire(key, 500)  # 86400


# Save action in Redis
async def save_action(chat_id: int, action: ActionsRedis):
    key = f"chat:{chat_id}:actions"
    await redis.lpush(key, action.model_dump_json())
    await redis.expire(key, 500)


async def get_message_by_id(chat_id: int, message_id: int):
    key = f"chat:{chat_id}:updates"
    messages = await redis.lrange(key, 0, -1)

    found = None
    for msg_raw in messages:
        msg = json.loads(msg_raw)
        if msg.get("message_id") == message_id:
            found = msg
    return found


# # get last update and message
# async def get_last_messages(chat_id: int, limit: int = 1):
#     key = f"chat:{chat_id}:messages"
#     messages = await redis.lrange(key, -limit, -1)
#     return [json.loads(m) for m in messages]


async def get_last_updates(chat_id: int, limit: int = 1):
    key = f"chat:{chat_id}:updates"
    updates = await redis.lrange(key, -limit, -1)
    return [json.loads(update) for update in updates]


# get and set scenarios from db
async def get_raw(key: str):
    value = await redis.get(key)
    return value.encode("utf-8") if value else None


async def set_raw(key: str, value: str, ex: int = 1000):
    await redis.set(key, value, ex=ex)
