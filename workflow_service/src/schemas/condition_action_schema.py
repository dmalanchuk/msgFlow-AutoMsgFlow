from pydantic import BaseModel


class ConditionAction(BaseModel):
    chat_id: int
    type: str
    params: dict
