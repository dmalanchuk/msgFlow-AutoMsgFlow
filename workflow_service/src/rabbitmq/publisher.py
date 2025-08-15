from src.config import settings
from src.rabbitmq.broker import broker


async def publish_action(action: dict):
    await broker.publish(action, settings.ACTION_QUEUE_NAME)
    print("Action published in action queue")
