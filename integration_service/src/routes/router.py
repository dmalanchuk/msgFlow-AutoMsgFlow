from faststream.rabbit.fastapi import RabbitRouter
from src.config import settings

router = RabbitRouter(settings.RABBITMQ_URL)
