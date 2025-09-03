from src.database import async_session
from src.logger import logger
from src.rabbitmq.publisher import publish_action
from src.services.pattern.condition_service import ConditionService
from src.services.pattern.event_service import EventService

from src.utils.get_user_email import get_user_email
from src.utils.get_chat_id import get_chat_id

from src.repositories.scenario_repo import (
    get_scenarios
)

from src.redis.redis_service import save_action


class ExecuteAction:
    @staticmethod
    async def execute_actions(chat_id: int, message_id: int):
        async with async_session() as session:
            event_service = EventService()
            condition_service = ConditionService(event_service)

            scenarios = await get_scenarios(chat_id, session)
            if not scenarios:
                logger.warning(f"No scenarios found for chat_id={chat_id}")
                return

            any_action_published = False

            for scenario in scenarios:
                is_condition_met = await condition_service.check_conditions_for_scenario(scenario, chat_id, message_id,
                                                                                         session)
                if is_condition_met:
                    actions = scenario.actions
                    if not isinstance(actions, list):
                        actions = [actions]

                    # if action - published action in redis and action_queue
                    for idx, action in enumerate(actions):
                        await save_action(chat_id, message_id, action)
                        # added index for message
                        await publish_action({
                            "chat_id": chat_id,
                            "message_id": message_id,
                            "index": idx,
                            "action": action
                        })
                    logger.info(f"Published {len(actions)} actions to queue and saved to Redis for chat_id={chat_id}")
                    any_action_published = True

            if not any_action_published:
                logger.info(f"Conditions not met for any scenario for chat_id={chat_id}")
