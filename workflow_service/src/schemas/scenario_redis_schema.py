from src.schemas.scenario_schema import EventCreate, ConditionCreate, ActionCreate
from pydantic import BaseModel


class ScenarioRedisGet(BaseModel):
    name: str
    chat_id: int
    event: list[EventCreate]
    condition: list[ConditionCreate]
    action: list[ActionCreate]
