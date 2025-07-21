from fastapi import Request, APIRouter
from typing import Any

from src.rabbitmq.publisher import publish_to_queue
from src.services.telegram_service import TelegramService

router = APIRouter()


@router.post("/telegram")
async def telegram_webhook(request: Request):
    body: dict[str, Any] = await request.json()
    update_type = await TelegramService.get_update_type(body)

    chat_id = await TelegramService.extract_chat_id(body, update_type)
    username = await TelegramService.extract_username(body, update_type)

    payload = {
        "source": "telegram",
        "update_type": update_type,
        "chat_id": chat_id,
        "username": username,
        "raw": body
    }

    # додаткові поля для конкретних типів
    if update_type == "message":
        payload["text"] = body["message"].get("text")

    elif update_type == "callback_query":
        payload["text"] = body["callback_query"].get("data")

    elif update_type == "inline_query":
        payload["query"] = body["inline_query"].get("query")

    elif update_type == "poll_answer":
        payload["poll_id"] = body["poll_answer"].get("poll_id")
        payload["answers"] = body["poll_answer"].get("option_ids")

    elif update_type == "chat_member":
        payload["new_status"] = body["chat_member"]["new_chat_member"].get("status")

    elif update_type == "chat_join_request":
        payload["user"] = body["chat_join_request"]["from"]

    await publish_to_queue(payload)
    return {"status": "ok"}

