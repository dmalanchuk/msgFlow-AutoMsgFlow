import aio_pika
import json
from integration_service.src.config import settings

QUEUE_NAME = "incoming.messages"

"""publish to rabbitmq, scenario"""


async def publish_to_scenario(payload: dict):
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(payload).encode(),
                content_type="application/json",
            ),
            routing_key=QUEUE_NAME,
        )
