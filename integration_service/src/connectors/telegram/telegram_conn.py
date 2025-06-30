from integration_service.src.rabbitmq.rabbit_producer import publish_to_scenario
import httpx
from fastapi import APIRouter, Request

KEYWORDS = ["замовлення"]  # потом вставляти з бд

router = APIRouter()


@router.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    data = await request.json()

    message = data.get("message")

    if not message:
        return {"status": "No message"}

    text = message.get("text", "")
    chat_id = message["chat"]["id"]
    username = message["from"].get("username", "")

    if any(keyword in text.lower() for keyword in KEYWORDS):
        await publish_to_scenario({
            "source": "telegram",
            "chat_id": chat_id,
            "username": username,
            "text": text
        })

    return {"status": "ok"}
