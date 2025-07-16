from src.schemas.condition_action_schema import ConditionAction
from src.schemas.event_schema import Event

from src.repositories.event_repo import EventRepo
from src.services.condition_service import ConditionService
from src.services.action_service import ActionService

from sqlalchemy.ext.asyncio import AsyncSession


class EventService:

    @staticmethod
    async def check_event(data: Event, session: AsyncSession):
        scenarios = await EventRepo.get_event(data, session)

        if not scenarios:
            return {"msg": "no scenario with this event"}

        results = []

        for scenario in scenarios:
            condition = scenario.conditions
            if not isinstance(condition, dict):
                continue

            condition_data = ConditionAction(
                type=condition.get("type"),
                params=condition.get("params")
            )

            condition_passed = await ConditionService.condition_contains_word(
                chat_id=data.chat_id,
                data=condition_data,
                session=session
            )

            if condition_passed.get("msg") == "scenario triggered":
                await ActionService.send_action_from_scenario(scenario)
                results.append(f"scenario {scenario.id} triggered")

        return {"results": results or ["no conditions matched"]}
