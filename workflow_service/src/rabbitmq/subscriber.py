from faststream.rabbit import RabbitBroker

from src.services.redis_service import ServiceRedis
from src.config import settings

broker = RabbitBroker(settings.RABBITMQ_URL)


# @broker.subscriber(settings.QUEUE_NAME)
# async def handle_incoming_message(message: dict):
#     try:
#         chat_id = message["chat_id"]
#         text = message["text"]
#
#         await ServiceRedis.save_update(chat_id, text)
#         print(f"Message saved in Redis for chat: {chat_id}")
#
#     except Exception as e:
#         print(f"Error saving message in Redis: {e}")


@broker.subscriber(settings.QUEUE_NAME)
async def handle_incoming_message(update: dict):
    try:
        chat_id = None
        update_type = "unknown"

        for key in [
            "message",
            "edited_message",
            "channel_post",
            "edited_channel_post",
            "inline_query",
            "chosen_inline_result",
            "callback_query",
            "shipping_query",
            "pre_checkout_query",
            "poll",
            "poll_answer",
            "my_chat_member",
            "chat_member",
            "chat_join_request"
        ]:
            if key in update:
                update_type = key
                break

        if update_type in ("message", "edited_message"):
            chat_id = update[update_type]["chat"]["id"]
        elif update_type in ("channel_post", "edited_channel_post"):
            chat_id = update[update_type]["chat"]["id"]
        elif update_type in ("my_chat_member", "chat_member", "chat_join_request"):
            chat_id = update[update_type]["chat"]["id"]
        elif update_type == "callback_query":
            chat_id = update["callback_query"]["message"]["chat"]["id"]

        if chat_id is not None:
            await ServiceRedis.save_update(chat_id, update)
            print(f"[{update_type}] saved for chat: {chat_id}")
        else:
            print(f"Не вдалося знайти chat_id для update_type: {update_type}")

    except Exception as e:
        print(f"Error saving message in Redis: {e}")


async def publish_action(action: dict):
    await broker.publish(action, settings.ACTION_QUEUE_NAME)
