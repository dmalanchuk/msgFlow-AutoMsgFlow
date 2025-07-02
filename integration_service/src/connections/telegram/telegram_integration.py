from fastapi import Request

from faststream.rabbit.fastapi import RabbitRouter
from src.services.event_builder import EventBuilder

router = RabbitRouter()


@router.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    body = await request.json()
    event = EventBuilder.build_event_from_telegram(body)

    if event:
        await router.broker.publish(event, queue="incoming.events")
        return {"status": f"Event {event['event_type']} sent"}

    return {"status": "Unsupported event"}
