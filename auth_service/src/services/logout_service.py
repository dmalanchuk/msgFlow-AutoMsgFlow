from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import Response
from src.repositories.refresh_tokens_repo import RefreshTokenRepo


class LogoutService:
    @staticmethod
    async def logout_service(request: Request, response: Response, session: AsyncSession):
        refresh_token = request.cookies.get("refresh_token")

        if not refresh_token:
            raise HTTPException(status_code=401, detail="Refresh token required")

        await RefreshTokenRepo.deactivate_refresh_token(refresh_token, response, session)
        return {"detail": "Successfully logout"}
