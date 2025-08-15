from src.config import settings
from src.database import async_session
from src.logger import logger
from src.services.get_chat_id_service import GetChatIdService
from src.redis.redis_service import ServiceRedis
from src.repositories.scenario_repo import ScenarioRepo
from src.services.pattern.condition_service import ConditionService
from src.services.pattern.event_service import EventService
from src.services.scenario_get_email_service import ScenarioGetEmailService
from src.services.scenario_service import ScenarioService
from src.rabbitmq.publisher import publish_action
from src.rabbitmq.broker import broker


@broker.subscriber(settings.QUEUE_NAME)
async def handle_incoming_message(message: dict):
    try:
        chat_id = message["chat_id"]
        raw_update = message["raw"]
        text = message.get("text")
        msg_id = (
                message.get("message_id") or
                raw_update.get("edited_message", {}).get("message_id") or
                raw_update.get("message", {}).get("message_id")
        )
        source = message["source"]
        event_type = message["update_type"]

        await ServiceRedis.save_update(chat_id, raw_update)
        if text:
            await ServiceRedis.save_message(chat_id, text, msg_id, source, event_type)
        logger.info(f"Update saved in Redis for chat: {chat_id}")

        async with async_session() as session:
            redis_service = ServiceRedis()
            scenario_repo = ScenarioRepo()
            get_chat_id_service = ScenarioGetEmailService()
            get_email_service = GetChatIdService()
            scenario_service = ScenarioService(scenario_repo, redis_service, get_chat_id_service, get_email_service)
            event_service = EventService(redis_service, scenario_repo, scenario_service)
            condition_service = ConditionService(redis_service, event_service, scenario_repo, scenario_service)

            scenarios = await scenario_repo.get_scenario(chat_id, session)
            if not scenarios:
                logger.warning(f"No scenarios found for chat_id={chat_id}")
                return

            any_action_published = False

            for scenario in scenarios:
                is_condition_met = await condition_service.check_conditions_for_scenario(scenario, chat_id, session)
                if is_condition_met:
                    actions = scenario.actions
                    if not isinstance(actions, list):
                        actions = [actions]

                    for action in actions:
                        await ServiceRedis.save_action(chat_id, action)
                        await publish_action({
                            "chat_id": chat_id,
                            "action": action
                        })
                    logger.info(f"Published {len(actions)} actions to queue and saved to Redis for chat_id={chat_id}")
                    any_action_published = True

            if not any_action_published:
                logger.info(f"Conditions not met for any scenario for chat_id={chat_id}")

    except Exception as e:
        logger.exception(f"Error saving message in Redis: {e}")
