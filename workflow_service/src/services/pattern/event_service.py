from pydantic import EmailStr

from src.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.redis.redis_service import get_last_updates
from src.repositories.scenario_repo import get_scenarios_all


async def check_event(
        email: EmailStr,
        session: AsyncSession
):
    try:
        updates = await get_last_updates(email, limit=1)
        event_matched = False

        if not updates:
            logger.info(f"No updates found for email: {email}")
            return None

        scenarios = await get_scenarios_all(email, session)
        for scenario in scenarios:
            if scenario.event.event_type == updates[0].event_type:
                event_matched = True
                return event_matched

        return event_matched

    except Exception as e:
        logger.exception(f"Failed to check event for email={email}")
        return {"msg": "Internal error", "error": str(e)}
