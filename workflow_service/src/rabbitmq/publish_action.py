from faststream.rabbit import RabbitBroker
from src.config import settings

broker = RabbitBroker(settings.RABBITMQ_URL)


async def publish_action(action: dict):
    await broker.publish(action, settings.ACTION_QUEUE_NAME)
