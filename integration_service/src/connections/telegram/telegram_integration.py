from fastapi import Request, APIRouter

from src.rabbitmq.publisher import publish_to_queue

router = APIRouter()


@router.post("/telegram")
async def telegram_webhook(request: Request):
    body = await request.json()

    message = body.get("message")

    if not message:
        return {"status": "no message"}

    chat = message.get("chat", {})
    from_user = message.get("from", {})
    text = message.get("text")

    if text:
        payload = {
            "text": text,
            "chat_id": chat.get("id"),
            "username": from_user.get("username"),
            "source": "telegram"
        }
        await publish_to_queue(payload)
        return {"status": "ok"}

    return {"status": "ignored"}
