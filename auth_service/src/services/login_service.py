from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from src.core.login_tokens import create_access_token, create_refresh_token
from src.repositories.login_repo import LoginRepo
from src.repositories.refresh_tokens_repo import RefreshTokenRepo
from src.schemas.user_schema import LoginUser
from src.config import settings

REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS


class LoginService:

    @staticmethod
    async def login_user_service(data: LoginUser, response: Response, session: AsyncSession):
        user = await LoginRepo.login_user_repo(data.email, data.password, session)

        access_token = create_access_token(data={"sub": data.email})
        refresh_token = create_refresh_token(data={"sub": data.email}, )

        await RefreshTokenRepo.save_refresh_token(user.id, refresh_token, session)

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        )

        return {"access_token": access_token}
