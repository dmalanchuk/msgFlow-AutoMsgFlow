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


@auth_router.post(
    "/register",
    summary="Register new user",
    description="Used to create a new user, with required fields: email, username, password",
    status_code=201,
    responses={
        409: {"description": "User is already registered"},
        400: {"description": "Invalid data in request state"},
    }
)
async def register_user(
        data: CreateUser = Body(...),
        session: AsyncSession = Depends(get_session)
):
    return await RegServices.reg_user_service(data, session)


@auth_router.post(
    "/login",
    summary="Login user",
    description="Used to login user, with required fields: email, password",
    status_code=200,
    responses={
        401: {"description": "Missing user email in request state"},
        404: {"description": "User not found"},
        400: {"description": "Invalid data in request state"},
    }
)
async def login_user(
        response: Response,
        data: LoginUser = Body(...),
        session: AsyncSession = Depends(get_session)
):
    return await LoginService.login_user_service(data, response, session)


@auth_router.delete(
    "/logout",
    summary="Logout user",
    description="Used to logout user",
    status_code=200,
    responses={
        401: {"description": "Refresh token required"},
    }
)
async def logout_user(
        request: Request,
        response: Response,
        session: AsyncSession = Depends(get_session)
):
    return await LogoutService.logout_service(request, response, session)


@auth_router.get(
    "/profile",
    summary="Get profile",
    description="Used to get info of user: username, email",
    status_code=200,
    responses={
        401: {"description": "Refresh token required"},
        404: {"description": "User not found"},
    }
)
async def get_profile(
        request: Request,
        session: AsyncSession = Depends(get_session)
):
    return await GetProfileService.get_profile_service(request, session)
