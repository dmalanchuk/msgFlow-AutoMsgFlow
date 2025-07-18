from src.services.redis_service import ServiceRedis
from src.schemas.condition_action_schema import ConditionAction
from src.repositories.condition_action_repo import ConditionActionRepo

from sqlalchemy.ext.asyncio import AsyncSession


class ConditionService:
    """
        the text is taken from Redis and checked for a condition,
        if it is found, the action is executed. Contains word condition.
    """

    @staticmethod
    async def receive_condition_from_scenario():
        ...
