from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.api.scenario_api import router
from src.api.debug_redis_api import router_debug
from src.rabbitmq.broker import broker
from src.rabbitmq.subscriber import handle_incoming_message
""" FastAPI app with RabbitMQ subscriber """


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await broker.connect()
    await broker.start()
    yield
    await broker.close()


app = FastAPI(lifespan=lifespan)
app.include_router(router, tags=["scenarios"])
app.include_router(router_debug, tags=["debug"])
