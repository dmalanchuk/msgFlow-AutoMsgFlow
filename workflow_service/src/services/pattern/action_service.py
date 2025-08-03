from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.scenario_repo import ScenarioRepo
from src.services.pattern.condition_service import ConditionService
from src.rabbitmq.subscriber import publish_action

from src.logger import logger


class ActionService:
    def __init__(
            self,
            scenarios_repo: ScenarioRepo,
            condition_service: ConditionService
    ):
        self.condition_service = condition_service
        self.scenarios_repo = scenarios_repo

    async def send_action_from_scenario(self, chat_id: int, session: AsyncSession):
        result = await self.condition_service.check_conditions(chat_id, session)

        if result:
            actions = await self.scenarios_repo.get_scenario(chat_id, session)

            for action in actions:
                await publish_action(action.actions)
                return {"msg": "Action sent", "action": action.actions}
        else:
            logger.info(f"Conditions false for chat_id={chat_id}")
            return {"msg": "conditions false"}

        return None
