from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users_model import UserModel
from src.schemas.user_schema import CreateUser

class regUser:


    @classmethod
    async def get_by_email(cls, email: EmailStr, session: AsyncSession):

        result = await session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        return result.scalars().first()

    @classmethod
    async def create_user(cls, data: CreateUser, session: AsyncSession):

        new_user = UserModel(**data)

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user

