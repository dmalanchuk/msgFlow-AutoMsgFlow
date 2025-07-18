from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.users_model import UserModel


class UserRepo:

    @staticmethod
    async def get_by_email(session: AsyncSession, email: str):
        result = await session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        return result.scalars().first()
