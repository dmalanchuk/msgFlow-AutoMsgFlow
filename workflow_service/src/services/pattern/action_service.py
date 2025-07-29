from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.scenario_repo import ScenarioRepo
from src.services.pattern.condition_service import ConditionService
from src.rabbitmq.subscriber import publish_action


class ActionService:

    @staticmethod
    async def send_action_from_scenario(chat_id: int, session: AsyncSession):
        result: bool = await ConditionService.check_conditions(chat_id, session)
        actions = await ScenarioRepo.get_scenario(chat_id, session)

        if result == True:
            for action in actions:
                await publish_action(action.actions)
                return {"msg": "Action sent", "action": action.actions}
        else:
            return {"msg": "conditions false"}

        return None
