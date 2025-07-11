

async def subscriber(channel):
    await channel.start_consuming()
