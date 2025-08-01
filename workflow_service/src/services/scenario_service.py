import json

from fastapi import Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.redis_service import ServiceRedis
from src.models.scenarios_model import ScenariosModel
from src.schemas.scenario_schema import ScenarioCreate

from src.repositories.scenario_repo import ScenarioRepo
from src.services.get_chat_id_service import GetChatIdService
from src.services.scenario_get_email_service import ScenarioGetEmailService

"""
    Business logic service for processing, creating, 
    storing scenarios of actions according to the ECA pattern
"""


class ScenarioService:

    @staticmethod
    async def create_scenario(
            session: AsyncSession,
            scenario: ScenarioCreate,
            scenarios_repo: ScenarioRepo,
            get_email_service: ScenarioGetEmailService,
            get_chat_id_service: GetChatIdService,
            request: Request
    ):

        try:
            chat_id = await get_chat_id_service.get_chat_id(scenario.chat_url)
            user_email = get_email_service.get_user_email(request)
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

        return await scenarios_repo.create_scenario(session, new_scenario)

    @staticmethod
    async def get_scenarios(
            chat_id: int,
            session: AsyncSession,
            scenarios_repo: ScenarioRepo,
            redis_service: ServiceRedis,
            ttl: int = 1000
    ):
        key = f"chat:{chat_id}:scenarios"

        cached = await redis_service.get_raw(key)
        if cached:
            return json.loads(cached)

        scenarios = await scenarios_repo.get_scenario(chat_id, session)

        to_cache = []
        for scenario in scenarios:
            to_cache.append({
                "event": scenario.event,
                "conditions": scenario.conditions,
                "actions": scenario.actions
            })

        await redis_service.set_raw(key, json.dumps(to_cache), ttl)
        return to_cache


