from faststream.rabbit import RabbitBroker
from src.config import settings

broker = RabbitBroker(settings.RABBITMQ_URL)


async def publish_to_queue(payload: dict):
    await broker.publish(payload, settings.QUEUE_NAME)
