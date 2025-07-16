from sqlalchemy.ext.asyncio import AsyncSession

from schemas.condition_action_schema import ConditionAction
from src.rabbitmq.publish_action import publish_action
from src.repositories.condition_action_repo import ConditionActionRepo

"""
    Create an action service on trigger words that will be sent to the broker and sent to the
    integration service, from there they will call functions
"""


class ActionService:

    @staticmethod
    async def send_action_from_scenario(scenario):
        action = scenario.actions

        if not isinstance(action, dict):
            return {"msg": "invalid action format"}

        action_type = action.get("type")
        action_params = action.get("params", {})

        if not action_type:
            return {"msg": "action type missing"}

        payload = {
            "type": action_type,
            "params": action_params,
            "scenario_id": scenario.id,
            "chat_id": scenario.chat_id,
        }

        await publish_action(payload)
        return {"msg": f"{action_type} action sent"}

    # async def action_send_message(chat_id: int, data: ConditionAction, session: AsyncSession):
    #     actions = await ConditionActionRepo.get_by_mode(chat_id, data, session, "actions")
    #
    #     if not actions:
    #         return {"msg": "No matching actions found"}
    #
    #     for scenario in actions:
    #         action = scenario.actions
    #
    #         action_type = action.get("type")
    #         action_params = action.get("params", {})
    #
    #         payload = {
    #             "type": action_type,
    #             "params": action_params,
    #             "scenario_id": scenario.id,
    #             "chat_id": scenario.chat_id,
    #         }
    #
    #         await publish_action(payload)
    #
    #     return {"msg": "send_message actions triggered"}
