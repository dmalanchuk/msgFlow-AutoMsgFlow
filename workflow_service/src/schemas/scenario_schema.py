from typing import Dict, Any, Literal, Optional
from pydantic import BaseModel, EmailStr

"""
    Scenario schema haver the same structure as in the database,
    and are used three unique classes for validation:
        - EventInfo
        - Condition
        - Action 
        
    This classes are used 'Literal' for validation, 
    and are used in the ScenarioCreate class for validation.  
"""


# class EventInfo(BaseModel):
#     type: Literal["message_received", "user_joined", "user_left", "new_post"]
#     source: Literal["telegram", "discord", "email"]  # add checking if email, add new column where u write your email
#
#
# class Condition(BaseModel):
#     type: Literal["contains_word", "equals"]
#     params: Dict[str, Any]
#
#
# class Action(BaseModel):
#     type: Literal["send_message", "forward"]
#     params: Dict[str, Any]
#
#
# class ScenarioCreate(BaseModel):
#     name: str
#     chat_url: str
#     owner_email: str
#     event: EventInfo
#     condition: Condition
#     action: Action
#
#     class Config:
#         from_attributes = True


# scenario patch update


# class ScenarioPatchUpdate(BaseModel):
#     name: Optional[str] = None
#     chat_url: Optional[str] = None
#     event: Optional[EventInfo] = None
#     conditions: Optional[Condition] = None
#     actions: Optional[Action] = None


# ============scenario schemas v2============


class ScenarioCreate(BaseModel):
    name: str
    chat_url: str
    owner_email: EmailStr
