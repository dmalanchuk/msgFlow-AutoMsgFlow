from src.repositories.scenario_repo import ScenarioRepo
from src.services.scenario_service import ScenarioService
from src.services.pattern.event_service import EventService
from src.services.pattern.condition_service import ConditionService
from src.services.redis_service import ServiceRedis

# class instance - because services used DI (dependency injection)
redis_service = ServiceRedis()
scenario_repo = ScenarioRepo()
scenario_service = ScenarioService(scenario_repo, redis_service)
event_service = EventService(redis_service, scenario_repo, scenario_service)
condition_service = ConditionService(redis_service, event_service, scenario_repo, scenario_service)
