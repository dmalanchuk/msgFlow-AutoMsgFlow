from faststream.rabbit import RabbitBroker
from src.config import settings

broker = RabbitBroker(settings.RABBITMQ_URL)