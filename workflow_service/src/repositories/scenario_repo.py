from typing import Coroutine

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

    @staticmethod
    async def create_scenario(session: AsyncSession, scenarios: ScenariosModel):
        session.add(scenarios)
        await session.commit()
        await session.refresh(scenarios)
        return scenarios

    @staticmethod
    async def get_by_name(name: str, session: AsyncSession):
        smtp = await session.execute(
            select(ScenariosModel).where(ScenariosModel.name == name)
        )

        return smtp.scalars().first()

    @staticmethod
    async def delete(scenario: Coroutine, session: AsyncSession):
        await session.delete(scenario)
        await session.commit()

    @staticmethod
    async def get_by_id(id: int, session: AsyncSession):
        smtp = await session.execute(
            select(ScenariosModel).where(ScenariosModel.id == id)
        )

        return smtp.scalars().one_or_none()

    @staticmethod
    async def update(scenario, session: AsyncSession):
        await session.commit()
        await session.refresh(scenario)
        return scenario
