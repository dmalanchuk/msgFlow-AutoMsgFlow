from pydantic import BaseModel


class Event(BaseModel):
    event_type: str
    chat_id: int
