from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.scenario_schema import ScenarioCreate
from src.models.scenarios_model import ScenariosModel


class ScenarioRepo:

    @staticmethod
    async def create_scenario(session: AsyncSession, scenario: ScenarioCreate):
        session.add(scenario)

        await session.commit()
        await session.refresh(scenario)
        return scenario
