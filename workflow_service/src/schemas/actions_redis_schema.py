from pydantic import BaseModel, EmailStr
from src.schemas.scenario_schema import ParamsSendMessage


class ActionsRedis(BaseModel):
    index: int
    email: EmailStr
    message_id: int
    type: str
    params: ParamsSendMessage
