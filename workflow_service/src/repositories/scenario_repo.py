from sqlalchemy.ext.asyncio import AsyncSession
from src.models.scenarios_model import ScenariosModel


class ScenarioRepo:

    @staticmethod
    async def create_scenario(session: AsyncSession, scenario: ScenariosModel):
        session.add(scenario)

        await session.commit()
        await session.refresh(scenario)
        return scenario
