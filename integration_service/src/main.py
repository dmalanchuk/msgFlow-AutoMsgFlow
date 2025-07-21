from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.routes.router import router
from src.rabbitmq.publisher import broker


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await broker.connect()
    await broker.start()
    yield
    await broker.close()


app = FastAPI(title="Integration Service", lifespan=lifespan)
app.include_router(router)
