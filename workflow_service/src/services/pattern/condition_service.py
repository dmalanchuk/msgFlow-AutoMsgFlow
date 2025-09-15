import json
import re
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session
from src.repositories.scenario_repo import get_scenarios_all_by_chat_id
from src.logger import logger
from src.redis.redis_service import get_message_by_id, get_last_updates
from src.services.pattern.event_service import check_event


# async def check_conditions(
#         chat_id: int,
#         session: AsyncSession
# ) -> bool:
#
#     result = await check_event(chat_id, session)
#
#     if not result:
#         logger.info(f"Event not matched for chat_id={chat_id}")
#         return False
#
#     text = await get_last_updates(chat_id)
#
#     if not text:
#         logger.warning(f"No messages found in Redis for chat_id={chat_id}")
#         return False
#     last_message = text[0]
#
#     conditions = await get_scenarios_all_by_chat_id(chat_id, session)
#
#     if result and last_message.get("text"):
#         for condition in conditions:
#             conditions_dict = condition.get("conditions") or {}
#             params = conditions_dict.get("params") or {}
#             word = params.get("word")
#
#             if word and word in last_message["text"]:
#                 return True
#
#     return False


async def check_conditions_for_scenario(
        scenario,
        chat_id: int,
        message_id: int
) -> bool:
    # Get last message in Redis
    messages = await get_message_by_id(chat_id, message_id)
    if not messages:
        logger.warning(f"No message in Redis for chat_id={chat_id}, message_id={message_id}")
        return False

    last_message = messages.get("text", "")
    logger.info(f"Message {message_id} from Redis: {last_message}")

    # Get conditions
    conditions_raw = scenario.conditions
    logger.info(f"Condition raw: {conditions_raw}")

    if not conditions_raw:
        return False

    if isinstance(conditions_raw, (list, tuple)):
        conditions = conditions_raw
    else:
        conditions = [conditions_raw]

    for cond in conditions:
        if isinstance(cond, str):
            try:
                cond = json.loads(cond)
            except json.JSONDecodeError:
                logger.error("Error parsing JSON in scenario.conditions")
                continue

        condition_type = cond.get("type") if isinstance(cond, dict) else getattr(cond, "type", None)
        condition_params = cond.get("params") if isinstance(cond, dict) else getattr(cond, "params", {})

        if condition_type == "contains_word":
            word = (condition_params.get("word") or "").lower()

            cleaned = re.sub(r"[^\w\s]", "", last_message.lower())
            words = cleaned.split()

            if word and word in words:
                logger.info(f"Match by contains_word: '{word}' found in '{last_message}'")
                return True
            else:
                logger.info(f"Word '{word}' not found in '{last_message}'")

    return False
