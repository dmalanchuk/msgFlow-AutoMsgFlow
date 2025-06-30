from integration_service.src.connectors.telegram.telegram_conn import get_updates
from integration_service.src.rabbitmq.rabbit_producer import publish_to_scenario
import asyncio


async def poll_telegram():
    last_update_id = None
    while True:
        updates = await get_updates(offset=last_update_id)
        for update in updates.get("result", []):
            message = update.get("message", {})
            chat_id = message["chat"]["id"]
            text = message.get("text", "")

            payload = {
                "chat_id": chat_id,
                "text": text,
                "source": "telegram"
            }
            await publish_to_scenario(payload)

            last_update_id = update["update_id"] + 1
        await asyncio.sleep(1)
