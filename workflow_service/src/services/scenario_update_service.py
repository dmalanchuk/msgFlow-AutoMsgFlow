from typing import Literal

from fastapi import HTTPException
from pydantic import EmailStr, BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.scenario_update_repo import update_scenario, update_scenario_component
from src.schemas.scenario_update_schema import UpdateScenario


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


async def update_scenario_component_service(
        name: str,
        email: EmailStr,
        body: BaseModel,
        session: AsyncSession,
        mode: Literal["events", "conditions", "actions"]
):
    body = body.model_dump(exclude_none=True)

    if not body:
        raise HTTPException(
            status_code=400, detail="Invalid request. Body cannot be empty"
        )

    scenario = await update_scenario_component(name, email, session, body, mode)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    return {"msg": "Scenario updated"}
