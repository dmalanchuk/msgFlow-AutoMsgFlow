import json

from fastapi import Request, HTTPException
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.get_chat_id import get_chat_id
from src.utils.get_user_email import get_user_email

from src.models.scenarios_model import ScenariosModel, EventsModel, ConditionsModel, ActionsModel
from src.schemas.scenario_schema import ScenarioCreate, ScenarioUpdate, EventCreate, ConditionCreate, ActionCreate
from src.schemas.scenario_redis_schema import ScenarioRedisGet

from src.repositories.scenario_repo import (
    create_scenario_repo, del_by_name, update_by_name, get_scenarios_all
)
from src.redis.redis_service import (
    set_raw, get_raw,
)

"""
    Business logic service for processing, creating, 
    storing scenarios of actions according to the ECA pattern
"""


# create scenarios
async def create_scenario_service(
        session: AsyncSession,
        scenario: ScenarioCreate,
        request: Request
):
    try:
        chat_id = await get_chat_id(scenario.chat_url)
        user_email = scenario.owner_email if scenario.owner_email else get_user_email(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    new_scenario = ScenariosModel(
        name=scenario.name,
        owner_email=user_email,
        chat_id=chat_id,
        events=[
            EventsModel(**event.model_dump())
            for event in scenario.event
        ],
        conditions=[
            ConditionsModel(**conditions.model_dump())
            for conditions in scenario.conditions
        ],
        actions=[
            ActionsModel(**actions.model_dump())
            for actions in scenario.actions
        ]
    )

    return await create_scenario_repo(session, new_scenario)


#
async def get_scenarios_service(
        email: EmailStr,
        session: AsyncSession,
):
    key = f"chat:{email}:scenarios"

    cached = await get_raw(key)
    if cached:
        return ScenarioRedisGet.model_validate_json(cached)

    scenarios = await get_scenarios_all(email, session)

    _to_cache = [
        ScenarioRedisGet(
            name=scenario.name,
            chat_id=scenario.chat_id,
            event=[
                EventCreate.model_validate(e) for e in scenario.events
            ],
            condition=[
                ConditionCreate.model_validate(c) for c in scenario.conditions
            ],
            action=[
                ActionCreate.model_validate(a) for a in scenario.actions
            ],
        )
        for scenario in scenarios
    ]

    await set_raw(key, json.dumps([s.model_dump() for s in _to_cache]))
    return _to_cache


# delete scenarios by name
async def delete_scenario_service(name: str, owner_email: EmailStr, session: AsyncSession):
    async with session.begin():
        scenario = await del_by_name(name, owner_email, session)

        if not scenario:
            raise HTTPException(status_code=404, detail="Scenario not found")
    return {"msg": "Scenario deleted"}


# update scenario
async def update_scenario_patch(name: str, owner_email: EmailStr, body: ScenarioUpdate,
                                session: AsyncSession):
    async with session.begin():
        body = body.model_dump(exclude_none=True)

        if not body:
            raise HTTPException(
                status_code=400, detail="Invalid request. Body cannot be empty"
            )

        scenario = await update_by_name(name, owner_email, body, session)
        if not scenario:
            raise HTTPException(status_code=404, detail="Scenario not found")

    return {"msg": "Scenario updated"}
