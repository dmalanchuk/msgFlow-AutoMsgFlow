from fastapi import Request

from faststream.rabbit.fastapi import RabbitRouter

router = RabbitRouter()


@router.post("/webhook/telegram")
async def order(request: Request):
    body = await request.json()

    return {"status": "ok"}
