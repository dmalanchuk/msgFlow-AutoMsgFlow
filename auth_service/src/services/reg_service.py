from fastapi import HTTPException
from pydantic.v1 import IntegerError

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users_model import UserModel
from src.schemas.user_schema import CreateUser
from src.repositories.reg_repo import RegUser
from src.core.security import hash_password


class RegServices:

    @staticmethod
    async def reg_user_service(data: CreateUser, session: AsyncSession):
        data.password = hash_password(data.password)
        new_user_model = UserModel(**data.model_dump())

        return await RegUser.create_user(new_user_model, session)
