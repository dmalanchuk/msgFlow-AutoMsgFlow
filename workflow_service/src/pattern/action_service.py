from sqlalchemy.ext.asyncio import AsyncSession
from src.rabbitmq.publisher import publish_action
from src.logger import logger

from src.repositories.scenario_repo import get_scenarios_all_by_chat_id

from src.redis.redis_service import save_action
from src.schemas.actions_redis_schema import ActionsRedis
from src.pattern.condition_service import check_conditions_for_scenario


async def execute_actions(chat_id: int, message_id: int, session: AsyncSession):
    scenarios = await get_scenarios_all_by_chat_id(chat_id, session)
    if not scenarios:
        logger.warning(f"No scenarios found for chat_id={chat_id}")
        return

    any_action_published = False

    for scenario in scenarios:
        is_condition_met = await check_conditions_for_scenario(scenario, chat_id, message_id)

        if not is_condition_met:
            continue

        actions_raw = getattr(scenario, "actions", None)
        if not actions_raw:
            logger.info(f"No actions found for scenario id={getattr(scenario, 'id', None)}")
            continue

        actions = actions_raw if isinstance(actions_raw, list) else [actions_raw]

        for idx, action in enumerate(actions):
            action_type = action.get("type") if isinstance(action, dict) else getattr(action, "type", None)
            action_params = action.get("params") if isinstance(action, dict) else getattr(action, "params", {})

            new_actions = ActionsRedis(
                index=idx,
                chat_id=chat_id,
                message_id=message_id,
                type=action_type,
                params=action_params
            )

            await save_action(chat_id, new_actions)

            await publish_action(new_actions)

        logger.info(f"Published {len(actions)} actions for chat_id={chat_id}")
        any_action_published = True

    if not any_action_published:
        logger.info(f"No actions published: conditions not met for any scenario for chat_id={chat_id}")
