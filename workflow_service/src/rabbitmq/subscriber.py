from src.rabbitmq.broker import broker
from src.schemas.event_schema import UpdateRaw

from src.config import settings
from src.logger import logger

from src.redis.redis_service import save_update


@broker.subscriber(settings.QUEUE_NAME)
async def handle_incoming_message_telegram(message: dict):
    try:
        chat_id = message["chat_id"]  # chat_id from telegram chat where a message was sent
        raw_update = message["raw"]  # raw update from the telegram
        source = message["source"]  # source usually telegram
        event_type = message["update_type"]  # event type: message, edited_message

        msg_id = (
                message.get("message_id")
                or raw_update.get("edited_message", {}).get("message_id")
                or raw_update.get("message", {}).get("message_id")
        )  # message_id from the message sent in a chat

        text = (
                message.get("text")
                or raw_update.get("edited_message", {}).get("text")
                or raw_update.get("message", {}).get("text")
        )  # text from a message sent in a chat

        new_update = UpdateRaw(
            event_type=event_type,
            chat_id=chat_id,
            source=source,
            text=text,
            message_id=msg_id
        )  # pydantic schema for save data in Redis

        await save_update(chat_id, new_update)
        logger.info(f"Update saved in Redis for chat: {new_update}")

        # if text:
        #     await save_message(chat_id, text, msg_id, source, event_type)
        #     logger.info(f"Update saved in Redis for chat: {chat_id}")

        # await ExecuteAction.execute_actions(chat_id, msg_id)

    except Exception as e:
        logger.exception(f"Error saving message in Redis: {e}")
