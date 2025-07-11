from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.api.scenario_api import router
from src.rabbitmq.subscriber import broker

""" FastAPI app with RabbitMQ subscriber """


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await broker.connect()
    yield
    await broker.close()


app = FastAPI(lifespan=lifespan)
app.include_router(router, tags=["scenarios"])
