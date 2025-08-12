from faststream.rabbit import RabbitBroker

from src.logger import logger
from src.services.redis_service import ServiceRedis
from src.config import settings

broker = RabbitBroker(settings.RABBITMQ_URL)


@broker.subscriber(settings.QUEUE_NAME)
async def handle_incoming_message(message: dict):
    try:
        chat_id = message["chat_id"]
        raw_update = message["raw"]
        text = message.get("text")
        msg_id = (
                message.get("message_id") or
                raw_update.get("edited_message", {}).get("message_id") or
                raw_update.get("message", {}).get("message_id")
        )
        source = message["source"]
        event_type = message["update_type"]

        await ServiceRedis.save_update(chat_id, raw_update)

        if text:
            await ServiceRedis.save_message(chat_id, text, msg_id, source, event_type)

        logger.debug(f"Update saved in Redis for chat: {chat_id}")

    except Exception as e:
        logger.error(f"Error saving message in Redis: {e}")


async def publish_action(action: dict):
    await broker.publish(action, settings.ACTION_QUEUE_NAME)
