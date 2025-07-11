from faststream.rabbit import RabbitBroker
from src.config import settings

broker = RabbitBroker(settings.RABBITMQ_URL)


@broker.subscriber(settings.QUEUE_NAME)
async def subscriber(channel):
    ...
