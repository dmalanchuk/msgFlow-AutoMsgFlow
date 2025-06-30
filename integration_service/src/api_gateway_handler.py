from fastapi import FastAPI, Request
from integration_service.src.rabbitmq.rabbit_producer import publish_to_scenario

app = FastAPI()


@app.post("/external-event")
async def handle_external_event(request: Request):
    payload = await request.json()
    await publish_to_scenario(payload)
    return {"status": "queued"}
