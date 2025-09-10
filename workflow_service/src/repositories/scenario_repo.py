from pydantic import EmailStr
from src.models.scenarios_model import ScenariosModel

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, and_, delete


async def get_scenario_chat_id(chat_id: int, session: AsyncSession):
    result = await session.execute(
        select(ScenariosModel).where(ScenariosModel.chat_id == chat_id)
    )
    return result.scalars().all()


# get all scenarios
async def get_scenarios_all(email: EmailStr, session: AsyncSession):
    result = await session.execute(
        select(ScenariosModel).where(
            ScenariosModel.owner_email == email
        )
        .options(
            selectinload(ScenariosModel.events),
            selectinload(ScenariosModel.conditions),
            selectinload(ScenariosModel.actions),
        )
    )
    return result.scalars().all()


async def create_scenario_repo(session: AsyncSession, scenarios: ScenariosModel):
    session.add(scenarios)
    await session.commit()
    await session.refresh(scenarios)
    return scenarios


async def del_by_name(name: str, owner_email: EmailStr, session: AsyncSession):
    async with session.begin():
        result = await session.execute(
            delete(ScenariosModel)
            .where(
                and_(
                    ScenariosModel.name == name,
                    ScenariosModel.owner_email == owner_email
                )
            )
            .returning(ScenariosModel.id)
        )
    return result.scalar_one_or_none()
