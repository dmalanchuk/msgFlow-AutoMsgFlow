import json

from fastapi import Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.redis.redis_service import ServiceRedis
from src.models.scenarios_model import ScenariosModel
from src.schemas.scenario_schema import ScenarioCreate, ScenarioPatchUpdate

from src.repositories.scenario_repo import ScenarioRepo
from src.utils.get_chat_id import get_chat_id
from src.utils.get_user_email import get_user_email

"""
    Business logic service for processing, creating, 
    storing scenarios of actions according to the ECA pattern
"""


class ScenarioService:
    def __init__(
            self,
            scenarios_repo: ScenarioRepo,
            redis_service: ServiceRedis,
    ):
        self.scenarios_repo = scenarios_repo
        self.redis_service = redis_service

    # create scenarios
    async def create_scenario(
            self,
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
            event=scenario.event.model_dump(),
            conditions=scenario.condition.model_dump(),
            actions=scenario.action.model_dump()

        )

        return await self.scenarios_repo.create_scenario(session, new_scenario)

    # needs refactoring: get scenarios
    async def get_scenarios(
            self,
            chat_id: int,
            session: AsyncSession,
            ttl: int = 1000
    ):
        key = f"chat:{chat_id}:scenarios"

        cached = await self.redis_service.get_raw(key)
        if cached:
            return json.loads(cached)

        scenarios = await self.scenarios_repo.get_scenarios(chat_id, session)

        to_cache = []
        for scenario in scenarios:
            to_cache.append({
                "chat_id": scenario.chat_id,
                "event": scenario.event,
                "conditions": scenario.conditions,
                "actions": scenario.actions
            })

        await self.redis_service.set_raw(key, json.dumps(to_cache), ttl)
        return to_cache

    # delete scenarios by name
    async def delete_scenario(self, name: str, owner_email: str, session: AsyncSession):
        async with session.begin():
            scenario = await self.scenarios_repo.del_by_name(name, owner_email, session)

            if not scenario:
                raise HTTPException(status_code=404, detail="Scenario not found")
        return {"msg": "Scenario deleted"}

    # update scenario
    async def update_scenario_patch(self, name: str, owner_email: str, body: ScenarioPatchUpdate,
                                    session: AsyncSession):
        async with session.begin():
            body = body.model_dump(exclude_none=True)

            if not body:
                raise HTTPException(
                    status_code=400, detail="Invalid request. Body cannot be empty"
                )

            scenario = await self.scenarios_repo.get_by_name_email(name, owner_email, body, session)
            if not scenario:
                raise HTTPException(status_code=404, detail="Scenario not found")

        return {"msg": "Scenario updated"}
