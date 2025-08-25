from pydantic import BaseModel


class Token(BaseModel):
    email: str
