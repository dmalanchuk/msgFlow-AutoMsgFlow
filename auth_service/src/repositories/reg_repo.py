from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users_model import UserModel

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

class RegUser:

    @staticmethod
    async def get_by_email(email: EmailStr, session: AsyncSession):
        result = await session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        return result.scalars().first()

    @staticmethod
    async def create_user(user: UserModel, session: AsyncSession):
        session.add(user)
        try:
            await session.commit()
            await session.refresh(user)
        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=409, detail="User is already registered!!")
        return user