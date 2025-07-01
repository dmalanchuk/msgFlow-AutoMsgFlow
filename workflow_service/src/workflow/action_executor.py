import httpx
from config import settings


async def execute_action(action: dict, data: dict):
    if action["type"] == "send_message":
        text = action["text"]
        chat_id = data["chat_id"]

        url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}

        async with httpx.AsyncClient() as client:
            await client.post(url, json=payload)
