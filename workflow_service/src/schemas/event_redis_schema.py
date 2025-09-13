from pydantic import BaseModel


class Event(BaseModel):
    event_type: str
    chat_id: int


class SaveUpdate(Event):
    source: str
    text: str
    message_id: int
