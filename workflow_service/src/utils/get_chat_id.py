import httpx
from src.config import settings

"""    
    Chat ID can only be pulled from public groups or channels, 
    from private channels is not yet available
"""

BOT_TOKEN = settings.TELEGRAM_TOKEN


async def get_chat_id(chat_url: str):
    if chat_url.startswith("https://t.me/"):
        chat_url = chat_url.replace("https://t.me/", "@")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChat"
    params = {"chat_id": chat_url}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()

        if not data["ok"]:
            raise ValueError("Invalid chat url")

        return data["result"]["id"]
