import aio_pika
import json
from integration_service.src.config import settings

"""publish to rabbitmq, scenario"""


async def publish_to_scenario(payload: dict):
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        await channel.declare_queue(settings.QUEUE_NAME, durable=True)
        message = aio_pika.Message(body=json.dumps(payload).encode())
        await channel.default_exchange.publish(message, routing_key=settings.QUEUE_NAME)
