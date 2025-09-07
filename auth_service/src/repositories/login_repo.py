from fastapi import HTTPException
from pydantic import EmailStr

from src.repositories.reg_repo import RegUser
from src.core.security import verify_password


class LoginRepo:
    @staticmethod
    async def login_user_repo(email: EmailStr, password: str, session):
        user = await RegUser.get_by_email(email, session)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        if not await verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Incorrect password")

        return user
