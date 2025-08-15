from typing import Dict, Any, Literal
from pydantic import BaseModel


"""
    Scenario schema haver the same structure as in the database,
    and are used three unique classes for validation:
        - EventInfo
        - Condition
        - Action 
        
    This classes are used 'Literal' for validation, 
    and are used in the ScenarioCreate class for validation.  
"""


class EventInfo(BaseModel):
    type: Literal["message_received", "user_joined", "user_left"]
    source: Literal["telegram", "discord", "email"]  # add checking if email, add new column where u write your email


class Condition(BaseModel):
    type: Literal["contains_word", "equals"]
    params: Dict[str, Any]


class Action(BaseModel):
    type: Literal["send_message", "forward"]
    params: Dict[str, Any]


class ScenarioCreate(BaseModel):
    name: str
    chat_url: str
    owner_email: str
    event: EventInfo
    condition: Condition
    action: Action

    class Config:
        from_attributes = True
