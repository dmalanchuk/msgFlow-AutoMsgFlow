from sqlalchemy.ext.asyncio import AsyncSession

from src.models.scenarios_model import ScenariosModel
from src.schemas.scenario_schema import ScenarioCreate

from src.repositories.scenario_repo import ScenarioRepo

"""
    Business logic service for processing, creating, 
    storing scenarios of actions according to the ECA pattern
"""


class ScenarioService:

    @staticmethod
    async def create_scenario(session: AsyncSession, scenario: ScenarioCreate):
        new_scenario = ScenariosModel(
            name=scenario.name,
            event=scenario.event.model_dump(),
            conditions=scenario.condition.model_dump(),
            actions=scenario.action.model_dump()
        )

        return await ScenarioRepo.create_scenario(session, new_scenario)
