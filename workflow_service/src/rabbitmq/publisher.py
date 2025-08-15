from src.config import settings
from src.logger import logger
from src.rabbitmq.subscriber import broker


async def publish_action(action: dict):
    await broker.publish(action, settings.ACTION_QUEUE_NAME)
    logger.info("Action published in action queue")
