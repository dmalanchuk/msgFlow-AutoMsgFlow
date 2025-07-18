from sqlalchemy.ext.asyncio import AsyncSession

from schemas.condition_action_schema import ConditionAction
from src.rabbitmq.subscriber import publish_action
from src.repositories.condition_action_repo import ConditionActionRepo

"""
    Create an action service on trigger words that will be sent to the broker and sent to the
    integration service, from there they will call functions
"""


class ActionService:

    @staticmethod
    async def send_action_from_scenario():
        ...
