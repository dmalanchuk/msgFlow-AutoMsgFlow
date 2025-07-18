from fastapi import Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

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
    async def create_scenario(session: AsyncSession, scenario: ScenarioCreate, request: Request):

        try:
            chat_id = await GetChatIdService.get_chat_id(scenario.chat_url)
            user_email = ScenarioGetEmailService.get_user_email(request)
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

        return await ScenarioRepo.create_scenario(session, new_scenario)
