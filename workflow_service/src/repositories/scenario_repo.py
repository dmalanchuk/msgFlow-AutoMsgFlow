from typing import Coroutine

from src.models.scenarios_model import ScenariosModel

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, delete


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
    async def del_by_name(name: str, session: AsyncSession):
        result = await session.execute(
            delete(ScenariosModel)
            .where(ScenariosModel.name == name)
            .returning(ScenariosModel.id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_name_email(name: str, email: str, session: AsyncSession):
        query = await session.execute(select(ScenariosModel).where(
                and_(
                    ScenariosModel.name == name,
                    ScenariosModel.owner_email == email
                )
            )
        )
        return query.scalars().one_or_none()

    @staticmethod
    async def update_scenario_patch(scenario: ScenariosModel, session: AsyncSession):
        await session.commit()
        await session.refresh(scenario)
        return scenario
