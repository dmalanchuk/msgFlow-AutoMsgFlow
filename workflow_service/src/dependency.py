from src.repositories.scenario_repo import ScenarioRepo

from src.services.scenario_service import ScenarioService

from src.services.pattern.event_service import EventService
from src.services.pattern.condition_service import ConditionService
from src.services.pattern.action_service import ActionService

from src.redis.redis_service import ServiceRedis

# class instance - because services used DI (dependency injection)

# repositories
scenario_repo = ScenarioRepo()

# services
redis_service = ServiceRedis()
scenario_service = ScenarioService(scenario_repo, redis_service)

# patterns
event_service = EventService(redis_service, scenario_repo, scenario_service)
condition_service = ConditionService(redis_service, event_service, scenario_repo, scenario_service)
action_service = ActionService(scenario_repo, condition_service)
