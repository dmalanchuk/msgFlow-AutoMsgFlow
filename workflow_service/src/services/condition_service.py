from src.services.redis_service import ServiceRedis
from src.schemas.condition_action_schema import ConditionAction
from src.repositories.condition_action_repo import ConditionActionRepo

from sqlalchemy.ext.asyncio import AsyncSession


class ConditionService:
    """
        the text is taken from Redis and checked for a condition,
        if it is found, the action is executed. Contains word condition.
    """

    @staticmethod
    async def condition_contains_word(chat_id: int, data: ConditionAction, session: AsyncSession):
        scenarios = await ConditionActionRepo.get_by_mode(chat_id, data, session, "conditions")
        messages = await ServiceRedis.get_last_messages(chat_id)

        if not messages:
            return {"msg": "no messages in chat"}

        last_message = messages[0]
        text = last_message["text", ""].lower()

        for scenario in scenarios:
            condition = scenario.conditions
            expected_word = condition["contains_word"]

            # write actions service
            if expected_word and expected_word.lower() in text:
                return {"msg": "scenario triggered"}

        return {"msg": "no scenario triggered"}
