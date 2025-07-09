from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


from starlette.requests import Request
from starlette.responses import Response

from src.repositories.refresh_tokens_repo import RefreshTokenRepo
from src.repositories.user_repo import UserRepo
from src.schemas.user_schema import CreateUser, LoginUser
from src.database import get_session
from src.services.login_service import LoginService
from src.services.reg_service import RegServices
from src.models.users_model import UserModel

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
async def logout_user(request: Request, response: Response, session: AsyncSession = Depends(get_session)):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token required")

    await RefreshTokenRepo.deactivate_refresh_token(refresh_token, response, session)
    return {"detail": "Successfully logout"}

@auth_router.get("/profile")
async def get_profile(
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    user_email = request.headers.get("X-User-Email")
    print("🧾 Отриманий X-User-Email:", user_email)
    if not user_email:
        raise HTTPException(status_code=400, detail="Missing user email in request state")

    # Знайти користувача по email
    user: UserModel | None = await UserRepo.get_by_email(session, user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "email": user.email,
        "username": user.username
    }
