from src.repositories.scenario_repo import ScenarioRepo

from src.services.scenario_service import ScenarioService

from src.services.pattern.event_service import EventService
from src.services.pattern.condition_service import ConditionService
from src.services.pattern.action_service import ActionService

from src.services.redis_service import ServiceRedis

from src.services.get_chat_id_service import GetChatIdService
from src.services.scenario_get_email_service import ScenarioGetEmailService

# class instance - because services used DI (dependency injection)
get_chat_id_service = GetChatIdService()
get_email_service = ScenarioGetEmailService()

# repositories
scenario_repo = ScenarioRepo()

# services
redis_service = ServiceRedis()
scenario_service = ScenarioService(scenario_repo, redis_service, get_email_service, get_chat_id_service)

# patterns
event_service = EventService(redis_service, scenario_repo, scenario_service)
condition_service = ConditionService(redis_service, event_service, scenario_repo, scenario_service)
action_service = ActionService(scenario_repo, condition_service)
