
from src.services.pattern.event_service import EventService
from src.services.pattern.condition_service import ConditionService
from src.services.pattern.action_service import ActionService


# class instance - because services used DI (dependency injection)


# patterns
event_service = EventService()
condition_service = ConditionService(event_service)
action_service = ActionService(condition_service)
