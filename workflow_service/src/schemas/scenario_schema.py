from typing import Any, Literal, Optional
from pydantic import BaseModel, EmailStr, Field
import re

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z]+$")

""""""


class ParamsContainsWord(BaseModel):
    word: str = Field(..., min_length=1, description="Key word for executing action")


class ScenarioCreate(BaseModel):
    name: str = Field(..., min_length=1,  max_length=16)
    chat_url: str
    owner_email: EmailStr

    class Config:
        from_attributes = True


class EventCreate(BaseModel):
    type: Literal["message_received", "user_joined", "user_left", "new_post"]
    source: Literal["telegram"]


class ConditionCreate(BaseModel):
    type: Literal["contains_word"]
    params: ParamsContainsWord


class ActionCreate(BaseModel):
    type: Literal["send_message", "forward"]
    params: dict[str, Any]


class ScenarioUpdate(BaseModel):
    name: Optional[str] = None
    chat_url: Optional[str] = None
    event: Optional[list[EventCreate]] = None
    conditions: Optional[list[ConditionCreate]] = None
    actions: Optional[list[ActionCreate]] = None
