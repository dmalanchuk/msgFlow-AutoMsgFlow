from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users_model import UserModel
from src.schemas.user_schema import CreateUser


class RegUser:

    @staticmethod
    async def get_by_email(email: EmailStr, session: AsyncSession):
        result = await session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        return result.scalars().first()

    @staticmethod
    async def create_user(user: UserModel, session: AsyncSession):
        # new_user = UserModel(**data.dict())
        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user
