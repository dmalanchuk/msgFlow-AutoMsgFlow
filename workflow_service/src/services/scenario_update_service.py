from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.scenario_update_repo import update_scenario, update_eca
from src.schemas.scenario_update_schema import UpdateScenario, UpdateEvent


async def update_scenario_service(
        name: str,
        email: EmailStr,
        body: UpdateScenario,
        session: AsyncSession
):
    body = body.model_dump(exclude_none=True)

    if not body:
        raise HTTPException(
            status_code=400, detail="Invalid request. Body cannot be empty"
        )

    scenario = await update_scenario(name, email, body, session)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    return {"msg": "Scenario updated"}


async def update_eca_service(
        name: str,
        email: EmailStr,
        body: UpdateEvent,
        session: AsyncSession
):
    body = body.model_dump(exclude_none=True)

    if not body:
        raise HTTPException(
            status_code=400, detail="Invalid request. Body cannot be empty"
        )

    scenario = await update_eca(name, email, body, session)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    return {"msg": "Scenario updated"}
