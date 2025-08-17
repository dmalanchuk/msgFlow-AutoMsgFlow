from src.repositories.scenario_repo import ScenarioRepo

from src.services.scenario_service import ScenarioService

from src.services.pattern.event_service import EventService
from src.services.pattern.condition_service import ConditionService
from src.services.pattern.action_service import ActionService

from src.redis.redis_service import ServiceRedis

from utils.get_chat_id import GetChatId
from utils.get_user_email import GetUserEmail

# class instance - because services used DI (dependency injection)
get_chat_id = GetChatId()
get_user_email = GetUserEmail()

# repositories
scenario_repo = ScenarioRepo()

# services
redis_service = ServiceRedis()
scenario_service = ScenarioService(scenario_repo, redis_service, get_user_email, get_chat_id)

# patterns
event_service = EventService(redis_service, scenario_repo, scenario_service)
condition_service = ConditionService(redis_service, event_service, scenario_repo, scenario_service)
action_service = ActionService(scenario_repo, condition_service)
