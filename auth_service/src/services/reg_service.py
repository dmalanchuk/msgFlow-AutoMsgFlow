from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user_schema import CreateUser
from src.repositories.reg_repo import regUser


class RegServices:

    @staticmethod
    async def reg_user_service(data: CreateUser, session: AsyncSession):
        new_user = await regUser.get_by_email(data.email, session)
        if new_user:
            raise HTTPException(status_code=409, detail="User is already registered!!")

        new_user = await regUser.create_user(data, session)
        return new_user