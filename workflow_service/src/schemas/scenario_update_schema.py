from pydantic import BaseModel
from typing import Optional, Literal

from src.schemas.scenario_schema import ParamsContainsWord, ParamsSendMessage


class UpdateScenario(BaseModel):
    name: Optional[str] = None
    chat_url: Optional[str] = None

    class Config:
        from_attributes = True


class UpdateEvent(BaseModel):
    type: Optional[Literal["message_received"]] = None
    source: Optional[Literal["telegram"]] = None

    class Config:
        from_attributes = True


class UpdateCondition(BaseModel):
    type: Optional[Literal["contains_word"]] = None
    params: Optional[ParamsContainsWord] = None

    class Config:
        from_attributes = True


class UpdateAction(BaseModel):
    type: Optional[Literal["send_message"]] = None
    params: Optional[ParamsSendMessage] = None

    class Config:
        from_attributes = True
