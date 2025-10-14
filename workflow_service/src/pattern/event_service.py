from src.repositories.scenario_repo import get_scenarios_all_by_chat_id
from src.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.redis.redis_service import get_last_updates


async def check_event(
        chat_id: int,
        session: AsyncSession
) -> bool | None:
    try:
        updates = await get_last_updates(chat_id, limit=1)

        if not updates:
            logger.info(f"No updates found for chat_id: {chat_id}")
            return None

        last_update = updates[0]
        event_type = last_update.get("event_type")

        scenarios = await get_scenarios_all_by_chat_id(chat_id, session)

        for scenario in scenarios:
            for event in scenario.events:
                if event.type == event_type:
                    logger.info(f"Matched event for chat_id={chat_id}, event_type={last_update.event_type}")
                    return True

        return False

    except Exception as e:
        logger.exception(f"Failed to check event for chat_id={chat_id}, error={e}")
        return False
