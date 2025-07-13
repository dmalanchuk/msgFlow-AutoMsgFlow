from typing import Literal

from src.models.scenarios_model import ScenariosModel
from src.schemas.condition_action_schema import ConditionAction

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_


class ConditionActionRepo:

    @staticmethod
    async def get_condition(data: ConditionAction, session: AsyncSession, mode: Literal["condition", "action"]):
        ...
