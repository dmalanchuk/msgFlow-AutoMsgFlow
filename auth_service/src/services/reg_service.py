from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users_model import UserModel
from src.schemas.user_schema import CreateUser
from src.repositories.reg_repo import RegUser
from src.core.security import hash_password


class RegServices:

    @staticmethod
    async def reg_user_service(data: CreateUser, session: AsyncSession):
        new_user = await RegUser.get_by_email(data.email, session)
        if new_user:
            raise HTTPException(status_code=409, detail="User is already registered!!")

        data.password = hash_password(data.password)
        new_user_model = UserModel(**data.model_dump())
        return await RegUser.create_user(new_user_model, session)
