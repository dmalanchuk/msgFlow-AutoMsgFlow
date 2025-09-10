from typing import Literal

from pydantic import EmailStr, BaseModel

from src.models.scenarios_model import ScenariosModel, EventsModel, ConditionsModel, ActionsModel

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, update, select


async def update_scenario(name: str, email: EmailStr, values: BaseModel, session: AsyncSession):
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


async def get_scenario(
        name: str,
        email: EmailStr,
        session: AsyncSession
):
    scenario = await session.execute(
        select(ScenariosModel).where(
            and_(
                ScenariosModel.name == name,
                ScenariosModel.owner_email == email
            )
        )
    )
    return scenario.scalars().first()


async def update_scenario_component(
        name: str,
        email: EmailStr,
        session: AsyncSession,
        values: BaseModel,
        mode: Literal["events", "conditions", "actions"]
):
    async with session.begin():
        scenario = await get_scenario(name, email, session)

        if mode == "events":
            query = await session.execute(
                update(EventsModel).values(**values).where(
                    EventsModel.scenario_id == scenario.id
                )
            )
        elif mode == "conditions":
            query = await session.execute(
                update(ConditionsModel).values(**values).where(
                    ConditionsModel.scenario_id == scenario.id
                )
            )
        elif mode == "actions":
            query = await session.execute(
                update(ActionsModel).values(**values).where(
                    ActionsModel.scenario_id == scenario.id
                )
            )

    return query.rowcount
