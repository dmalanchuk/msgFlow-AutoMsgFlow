from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from src.schemas.user_schema import CreateUser
from src.database import get_session
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
