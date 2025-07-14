from typing import Literal

from src.models.scenarios_model import ScenariosModel
from src.schemas.condition_action_schema import ConditionAction

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_


class ConditionActionRepo:
    """
        query in table scenarios by condition or action type and params
    """

    @staticmethod
    async def get_by_mode(data: ConditionAction, session: AsyncSession, mode: Literal["conditions", "actions"]):
        field = getattr(ScenariosModel, mode)

        query = await session.execute(
            select(ScenariosModel).where(
                and_(
                    ScenariosModel.chat_id == data.chat_id,
                    field['type'].astext == data.type,
                    field['params'].astext == data.params
                )
            )
        )

        return query.scalars().all()
