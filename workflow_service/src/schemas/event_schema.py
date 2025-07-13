from pydantic import BaseModel


class Event(BaseModel):
    source: str
    type: str
    text: str
    chat_id: int
