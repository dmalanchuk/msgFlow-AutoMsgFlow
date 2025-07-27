from src.schemas.condition_action_schema import ConditionAction
from src.repositories.condition_action_repo import ConditionActionRepo
from src.decorators import timer

from sqlalchemy.ext.asyncio import AsyncSession


class ConditionService:

    @staticmethod
    @timer
    async def receive_condition():
        ...
