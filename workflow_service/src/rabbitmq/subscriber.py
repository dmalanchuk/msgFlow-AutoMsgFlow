from faststream.rabbit import RabbitBroker

from src.services.redis_service import ServiceRedis
from src.config import settings

broker = RabbitBroker(settings.RABBITMQ_URL)


@broker.subscriber(settings.QUEUE_NAME)
async def handle_incoming_message(message: dict):
    try:
        chat_id = message["chat_id"]
        text = message["text"]

        await ServiceRedis.save_message(chat_id, text)
        print(f"Message saved in Redis for chat: {chat_id}")

    except Exception as e:
        print(f"Error saving message in Redis: {e}")


async def publish_action(action: dict):
    await broker.publish(action, settings.ACTION_QUEUE_NAME)
