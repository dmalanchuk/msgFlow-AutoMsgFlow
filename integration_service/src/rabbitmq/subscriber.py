from src.config import settings
from src.rabbitmq.broker import broker
from src.services.execute_action_service import ExecuteActionService


@broker.subscriber(settings.ACTION_QUEUE_NAME)
async def handle_workflow_response(payload: dict):
    print("[DEBUG] Received from RabbitMQ:", payload)
    chat_id = payload.get("chat_id")
    if not chat_id:
        print("No chat_id in payload")
        return

    await ExecuteActionService.execute_action(chat_id)