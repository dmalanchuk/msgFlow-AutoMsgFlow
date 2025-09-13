import json

from src.logger import logger
from src.redis.redis_client import redis
from src.services.sender import send_message


class ExecuteActionService:

    @staticmethod
    async def execute_action(chat_id: int, action: dict | None = None):
        if action is None:
            redis_key = f"chat:{chat_id}:action"
            action_raw = await redis.lindex(redis_key, 0)
            if not action_raw:
                logger.warning(f"No action found in Redis for chat_id{chat_id}")
                return
            try:
                action_payload = json.loads(action_raw)
                action = action_payload.get("action", {})
            except json.JSONDecodeError:
                logger.error(f"Incorrect json in redis for chat_id{chat_id}")
                return

        action_type = action.get("type")
        params = action.get("params", {})

        if action_type == "send_message":
            text = params.get("text")
            if not text:
                logger.info(f"Missing text in action for chat_id: {chat_id}")
                return

            await send_message(chat_id, text)
            logger.info(f"Send message to Telegram in chat_id: {chat_id}")

        else:
            logger.error(f"Incorrect action type {action.get("type"), action_type}")
