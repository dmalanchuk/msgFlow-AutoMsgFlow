from src.models.scenarios_model import ScenariosModel

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class ScenarioRepo:

    @staticmethod
    async def get_scenario(chat_id: int, session: AsyncSession):
        result = await session.execute(
            select(ScenariosModel).where(ScenariosModel.chat_id == chat_id)
        )
        return result.scalars().all()
