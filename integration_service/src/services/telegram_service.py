from typing import Any
from src.logger import logger


# needs full refactoring
class TelegramService:

    @staticmethod
    async def get_update_type(update: dict[str, Any]) -> str:
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
            "new_chat_member",
            "left_chat_member",
            "chat_member",
            "chat_join_request"
        ]:
            if key in update:
                return key
        return "unknown"

    @staticmethod
    async def extract_chat_id(update: dict[str, Any], update_type: str) -> int | None:
        try:
            if update_type in ("message", "edited_message", "channel_post", "edited_channel_post"):
                return update[update_type]["chat"]["id"]
            elif update_type in ("callback_query",):
                return update["callback_query"]["message"]["chat"]["id"]
            elif update_type in ("chat_member", "my_chat_member", "chat_join_request"):
                return update[update_type]["chat"]["id"]
        except Exception as e:
            logger.exception(f"Failed to extract chat_id from update: {e}")
            return None

    @staticmethod
    async def extract_username(update: dict[str, Any], update_type: str) -> str | None:
        try:
            if update_type in ("message", "edited_message"):
                return update[update_type]["from"].get("username")
            elif update_type == "callback_query":
                return update["callback_query"]["from"].get("username")
            elif update_type == "inline_query":
                return update["inline_query"]["from"].get("username")
            elif update_type == "chat_join_request":
                return update["chat_join_request"]["from"].get("username")
            elif update_type == "chat_member":
                return update["chat_member"]["from"].get("username")
        except Exception as e:
            logger.exception(f"Failed to extract username from update: {e}")
            return None
