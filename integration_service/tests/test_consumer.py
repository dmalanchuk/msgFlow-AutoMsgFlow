import asyncio
import aio_pika


async def test_rabbit():
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    print("Підключення до RabbitMQ успішне")
    await connection.close()

asyncio.run(test_rabbit())
