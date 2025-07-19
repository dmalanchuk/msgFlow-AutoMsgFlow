from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import Response
from src.repositories.refresh_tokens_repo import RefreshTokenRepo
from src.schemas.user_schema import CreateUser, LoginUser
from src.database import get_session
from src.services.get_profile_service import GetProfileService
from src.services.login_service import LoginService
from src.services.logout_service import LogoutService
from src.services.reg_service import RegServices

auth_router = APIRouter(
    prefix="/auth",
)


@auth_router.post("/register")
async def register_user(
        data: CreateUser = Body(...),
        session: AsyncSession = Depends(get_session)
):
    return await RegServices.reg_user_service(data, session)


@auth_router.post("/login")
async def login_user(
        response: Response,
        data: LoginUser = Body(...),
        session: AsyncSession = Depends(get_session)
):
    return await LoginService.login_user_service(data, response, session)


@auth_router.post("/logout")
async def logout_user(
        request: Request,
        response: Response,
        session: AsyncSession = Depends(get_session)
):
    return await LogoutService.logout_service(request, response, session)


@auth_router.get("/profile")
async def get_profile(
        request: Request,
        session: AsyncSession = Depends(get_session)
):
    return await GetProfileService.get_profile_service(request, session)
