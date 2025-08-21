import json

from src.config import settings
from src.logger import logger
from src.rabbitmq.broker import broker
from src.services.execute_action_service import ExecuteActionService


@broker.subscriber(settings.ACTION_QUEUE_NAME)
async def handle_workflow_response(payload: dict):
    logger.info("Received from RabbitMQ:", payload)
    chat_id = payload.get("chat_id")
    if not chat_id:
        logger.warning("No chat_id in payload")
        return

    action = payload.get("action")

    # Check, if this a dict
    if not isinstance(action, dict):
        logger.error(f"Action is not a dict: {action}")
        return

    await ExecuteActionService.execute_action(chat_id, action)