from pydantic import EmailStr
from src.models.scenarios_model import ScenariosModel
from src.schemas.scenario_schema import ScenarioUpdate

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_


# needs refactoring
async def update_by_name(name: str, email: EmailStr, values: dict, session: AsyncSession):
    query = await session.execute(
        update(ScenariosModel).values(**values).where(
            and_(
                ScenariosModel.name == name,
                ScenariosModel.owner_email == email
            )
        )
    )
    return query.scalars().one_or_none()
