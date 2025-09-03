from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users_model import UserModel


class RegUser:

    @staticmethod
    async def create_user(user: UserModel, session: AsyncSession):
        session.add(user)
        try:
            await session.commit()
            await session.refresh(user)
        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=409, detail="User is already registered!!")
