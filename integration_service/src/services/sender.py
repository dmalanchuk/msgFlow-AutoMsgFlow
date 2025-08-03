import httpx
from src.config import settings

"""To send a message to the chat bot"""

BOT_TOKEN = settings.TELEGRAM_TOKEN
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

async def send_message(chat_id: int, text: str):
    async with httpx.AsyncClient() as client:
        await client.post(BASE_URL, json={
            "chat_id": chat_id,
            "text": text
        })