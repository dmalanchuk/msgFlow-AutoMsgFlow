from pydantic import BaseModel


class Event(BaseModel):
    source: str
    event_type: str
    chat_id: int
    text: str
