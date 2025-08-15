from faststream.rabbit import RabbitBroker

from src.config import settings
from src.database import async_session
from src.logger import logger
from src.services.execute_action import ExecuteAction
from src.services.get_chat_id_service import GetChatIdService
from src.redis.redis_service import ServiceRedis
from src.repositories.scenario_repo import ScenarioRepo
from src.services.pattern.condition_service import ConditionService
from src.services.pattern.event_service import EventService
from src.services.scenario_get_email_service import ScenarioGetEmailService
from src.services.scenario_service import ScenarioService


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
        logger.info(f"Update saved in Redis for chat: {chat_id}")

        await ExecuteAction.execute_actions(chat_id)

    except Exception as e:
        logger.exception(f"Error saving message in Redis: {e}")

async def publish_action(action: dict):
    await broker.publish(action, settings.ACTION_QUEUE_NAME)
    logger.info("Action published in action queue")
