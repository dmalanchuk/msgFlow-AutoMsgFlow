from src.config import settings
from src.rabbitmq.broker import broker


async def publish_to_queue(payload: dict):
    await broker.publish(payload, settings.QUEUE_NAME)
