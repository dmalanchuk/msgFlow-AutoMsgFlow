from typing import Literal, Optional
from pydantic import BaseModel, EmailStr, Field, field_validator

import re

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z ]+$")
ALLOWED_DOMAINS = ["gmail.com", "ukr.net"]


class ParamsContainsWord(BaseModel):
    word: str = Field(..., min_length=1, description="Key word for executing action")


class ParamsSendMessage(BaseModel):
    text: str = Field(..., min_length=1, max_length=40, description="Text for sending message")


class EventCreate(BaseModel):
    type: Literal["message_received"]
    source: Literal["telegram"]

    class Config:
        from_attributes = True


class ConditionCreate(BaseModel):
    type: Literal["contains_word"]
    params: ParamsContainsWord

    class Config:
        from_attributes = True


class ActionCreate(BaseModel):
    type: Literal["send_message"]
    params: ParamsSendMessage

    class Config:
        from_attributes = True


class ScenarioCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=16)
    chat_url: str
    owner_email: EmailStr
    event: list[EventCreate]
    conditions: list[ConditionCreate]
    actions: list[ActionCreate]

    @field_validator("name")
    def validate_name(cls, name: str) -> str:
        if not LETTER_MATCH_PATTERN.match(name):
            raise ValueError("Name must contain only letters")
        return name

    @field_validator("owner_email")
    def validate_owner_email(cls, email: EmailStr) -> EmailStr:
        domain = str(email).rpartition("@")[2].lower()
        if domain not in ALLOWED_DOMAINS:
            raise ValueError("Email must be from gmail.com or ukr.net")
        return email

    class Config:
        from_attributes = True


class ScenarioUpdate(BaseModel):
    name: Optional[str] = None
    chat_url: Optional[str] = None
    event: Optional[list[EventCreate]] = None
    conditions: Optional[list[ConditionCreate]] = None
    actions: Optional[list[ActionCreate]] = None
