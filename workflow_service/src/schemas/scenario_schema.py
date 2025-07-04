from typing import Dict, Any, Literal
from pydantic import BaseModel

"""
Example for EventInfo:
    {
      "type": "message_received",
      "source": "telegram"
    }   
"""


class EventInfo(BaseModel):
    type: Literal["message_received", "user_joined", "reaction_added"]
    source: Literal["telegram", "discord", "email", "notion"]


"""
1. Example for Condition:
    {
      "type": "contains_word",
      "params": {
        "word": "замовлення"
      }
    }
2. Example for Condition:    
    {
      "type": "starts_with",
      "params": {
        "prefix": "Привіт"
      }
    }
"""


class Condition(BaseModel):
    type: Literal["contains_word", "starts_with", "equals"]
    params: Dict[str, Any]


"""
1. Example for Action:  
    {
      "type": "send_message",
      "params": {
        "chat_id": 123456789,
        "text": "Дякуємо за ваше замовлення!"
      }
    }
"""


class Action(BaseModel):
    type: Literal["send_message", "forward", "notion_record"]
    params: Dict[str, Any]


class ScenarioCreate(BaseModel):
    name: str
    chat_id: int
    event: EventInfo
    condition: Condition
    action: Action

    class Config:
        from_attributes = True
