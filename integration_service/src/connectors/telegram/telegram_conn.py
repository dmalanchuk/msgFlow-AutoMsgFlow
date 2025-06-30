from integration_service.src.config import settings
import httpx

BOT_TOKEN = settings.TELEGRAM_TOKEN
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


async def send_message(chat_id: id, message: str):
    url = f"{BASE_URL}/sendMessage"
    params = {"chat_id": chat_id, "text": message}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, params=params)

        return response.json()


async def get_updates(offset: int = None):
    url = f"{BASE_URL}/getUpdates"
    params = {"timeout": 100}

    if offset is not None:
        params["offset"] = offset

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

        return response.json()
