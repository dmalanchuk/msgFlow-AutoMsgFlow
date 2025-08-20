from src.rabbitmq.broker import broker
from src.config import settings
from src.logger import logger
from src.services.execute_action_service import ExecuteAction
from src.redis.redis_service import ServiceRedis


@broker.subscriber(settings.QUEUE_NAME)
async def handle_incoming_message(message: dict):
    try:
        chat_id = message["chat_id"]
        raw_update = message["raw"]
        # text = message.get("text")

        msg_id = (
                message.get("message_id") or
                raw_update.get("edited_message", {}).get("message_id") or
                raw_update.get("message", {}).get("message_id")
        )
        source = message["source"]
        event_type = message["update_type"]

        text = (
                message.get("text")
                or raw_update.get("edited_message", {}).get("text")
                or raw_update.get("message", {}).get("text")
        )

        await ServiceRedis.save_update(chat_id, raw_update)
        if text:
            await ServiceRedis.save_message(chat_id, text, msg_id, source, event_type)
            logger.info(f"Update saved in Redis for chat: {chat_id}")

            await ExecuteAction.execute_actions(chat_id, msg_id)

    except Exception as e:
        logger.exception(f"Error saving message in Redis: {e}")

