from src.repositories.scenario_repo import ScenarioRepo

from sqlalchemy.ext.asyncio import AsyncSession


class ConditionService:

    @staticmethod
    async def receive_condition(chat_id: int, session: AsyncSession):
        scenario = await ScenarioRepo.get_scenario(chat_id, session)

        return scenario
