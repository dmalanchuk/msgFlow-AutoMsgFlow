from typing import Dict, Any, Literal
from pydantic import BaseModel


class EventInfo(BaseModel):
    type: Literal["message_received", "user_joined", "reaction_added"]
    source: Literal["telegram", "discord", "email", "notion"]


class Condition(BaseModel):
    type: Literal["contains_word", "starts_with", "equals"]
    params: Dict[str, Any]


class Action(BaseModel):
    type: Literal["send_message", "forward", "notion_record"]
    params: Dict[str, Any]


class ScenarioCreate(BaseModel):
    name: str
    chat_url: str
    event: EventInfo
    condition: Condition
    action: Action

    class Config:
        from_attributes = True
