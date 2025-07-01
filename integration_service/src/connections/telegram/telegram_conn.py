from fastapi import Request

from faststream.rabbit.fastapi import RabbitRouter

router = RabbitRouter()


@router.post("/webhook/telegram")
async def order(request: Request):
    body = await request.json()
    event_type = None
    event_data = {}

    if "message" in body:
        msg = body["message"]
        chat = msg.get("chat", {})
        user = msg.get("from", {})

        event_data = {
            "chat_id": chat.get("id"),
            "user_id": user.get("id"),
            "message_id": msg.get("message_id"),
            "username": user.get("username", "")
        }

        if "text" in msg:
            event_type = "telegram.message_received"
            event_data["text"] = msg["text"]
        elif "photo" in msg:
            event_type = "telegram.photo_received"
            event_data["caption"] = msg.get("caption", "")

    if event_type:
        event = {
            "event_type": event_type,
            "source": "telegram",
            "data": event_data
        }

        await router.broker.publish(event, queue="incoming.events")
        return {"status": f"Event {event_type} sent to broker"}

    return {"status": "Unsupported event type"}
