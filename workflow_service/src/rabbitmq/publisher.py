from src.config import settings
from src.rabbitmq.broker import broker
from src.schemas.actions_redis_schema import ActionsRedis


async def publish_action(action: ActionsRedis):
    await broker.publish(action, settings.ACTION_QUEUE_NAME)
