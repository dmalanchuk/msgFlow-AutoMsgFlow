from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from starlette.requests import Request
from starlette.responses import Response

from src.repositories.refresh_tokens_repo import RefreshTokenRepo
from src.schemas.user_schema import CreateUser, LoginUser
from src.database import get_session
from src.services.login_service import LoginService
from src.services.reg_service import RegServices

auth_router = APIRouter(
    prefix="/auth",
)

@auth_router.post("/register")
async def register_user(
    data: Annotated[CreateUser, Depends()],
    session: AsyncSession = Depends(get_session)
):
    return await RegServices.reg_user_service(data, session)

@auth_router.post("/login")
async def login_user(
    data: Annotated[LoginUser, Depends()],
    response: Response,
    session: AsyncSession = Depends(get_session)
):
    return await LoginService.login_user_service(data, response, session)

@auth_router.post("/logout")
async def logout_user(request: Request, response: Response, session: AsyncSession = Depends(get_session)):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token required")

    await RefreshTokenRepo.deactivate_refresh_token(refresh_token, response, session)
    return {"detail": "Successfully logout"}
