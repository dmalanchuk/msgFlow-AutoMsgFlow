from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    email: EmailStr
    username: str


class CreateUser(User):
    password: str = Field(min_length=8)
