from datetime import datetime, timedelta, timezone

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Response

from src.models.login_tokens_model import LoginTokens
from src.config import settings

REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS


class RefreshTokenRepo:

    @staticmethod
    async def save_refresh_token(user_id: int, refresh_token: str, session: AsyncSession):

        aware_now = datetime.now(timezone.utc)
        expires_at = aware_now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

        naive_now = aware_now.replace(tzinfo=None)
        naive_exp = expires_at.replace(tzinfo=None)

        token = LoginTokens(
            user_id=user_id,
            refresh_token=refresh_token,
            is_active=True,
            created_at=naive_now,
            expires_at=naive_exp
        )

        session.add(token)
        await session.commit()
        await session.refresh(token)
        return token

    @staticmethod
    async def is_active_token(refresh_token: str, response: Response, session: AsyncSession):

        if not refresh_token:
            raise HTTPException(status_code=401, detail="Refresh token is required")

        stmt = (
            update(LoginTokens)
            .where(LoginTokens.refresh_token == refresh_token)
            .values(is_active=True)
        )

        await session.execute(stmt)
        await session.commit()

        response.delete_cookie("refresh_token")

    @staticmethod
    async def deactivate_refresh_token(refresh_token: str, response: Response, session: AsyncSession):

        if not refresh_token:
            raise HTTPException(status_code=401, detail="Refresh token required")

        stmt = (
            update(LoginTokens)
            .where(LoginTokens.refresh_token == refresh_token)
            .values(is_active=False)
        )

        await session.execute(stmt)
        await session.commit()

        response.delete_cookie("refresh_token")

    @staticmethod
    async def get_token(refresh_token: str, session: AsyncSession):

        result = await session.execute(
            select(LoginTokens).where(LoginTokens.refresh_token == refresh_token)
        )
        return result.scalars().first()

    @staticmethod
    async def get_valid_token(refresh_token: str, session: AsyncSession):

        token = await RefreshTokenRepo.get_token(refresh_token, session)
        now = datetime.now(timezone.utc)

        if not token or token.is_active or token.expires_at < now:
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

        return token
