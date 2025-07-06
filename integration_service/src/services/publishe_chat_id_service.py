import json
from faststream.rabbit import RabbitBroker
from src.config import settings

broker = RabbitBroker(settings.RABBITMQ_URL)


async def publish_chat_id(chat_id: int):
    message = {
        "chat_id": chat_id,
        "name": "default",
        "event": {"type": "none", "source": "none"},
        "conditions": {"type": "none", "params": {}},
        "actions": {"type": "none", "params": {}}
    }
    await broker.publish(message, routing_key="scenario.register")
