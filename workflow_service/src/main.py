from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.api.scenario_api import router
from src.rabbitmq.broker import broker
from src.rabbitmq.subscriber import handle_incoming_message_telegram


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await broker.connect()
    await broker.start()
    yield
    await broker.close()


app = FastAPI(lifespan=lifespan, title="Workflow Service")
app.include_router(router, tags=["scenarios"])
