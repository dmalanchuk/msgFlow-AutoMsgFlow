from src.schemas.condition_action_schema import ConditionAction
from src.repositories.condition_action_repo import ConditionActionRepo

from sqlalchemy.ext.asyncio import AsyncSession


class ConditionService:

    @staticmethod
    async def receive_condition(chat_id: int, data: ConditionAction, session: AsyncSession):
        conditions = await ConditionActionRepo.get_by_mode(chat_id, data, session, "conditions")

        return conditions
