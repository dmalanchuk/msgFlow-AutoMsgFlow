from pydantic import EmailStr

from src.models.scenarios_model import ScenariosModel, EventsModel

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, update, select


async def update_scenario(name: str, email: EmailStr, values: dict, session: AsyncSession):
    async with session.begin():
        query = await session.execute(
            update(ScenariosModel).values(**values).where(
                and_(
                    ScenariosModel.name == name,
                    ScenariosModel.owner_email == email
                )
            )
        )
    return query.rowcount


async def update_eca(
        name: str,
        email: EmailStr,
        values: dict,
        session: AsyncSession
):
    async with session.begin():
        scenario = await session.execute(
            select(ScenariosModel).where(
                and_(
                    ScenariosModel.name == name,
                    ScenariosModel.owner_email == email
                )
            )
        )
        scenario = scenario.scalars().first()
        if not scenario:
            return None

        query = await session.execute(
            update(EventsModel).values(**values).where(
                EventsModel.scenario_id == scenario.id
            )
        )
    return query.rowcount
