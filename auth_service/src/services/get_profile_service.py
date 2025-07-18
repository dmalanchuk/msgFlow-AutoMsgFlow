from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from src.repositories.user_repo import UserRepo
from src.models.users_model import UserModel


class GetProfileService:
    @staticmethod
    async def get_profile_service(request: Request, session: AsyncSession):

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
