from pydantic import BaseModel
from src.enums.event_enum import EventType


class Event(BaseModel):
    event_type: EventType
    chat_id: int
