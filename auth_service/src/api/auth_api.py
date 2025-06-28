from fastapi import APIRouter

auth_router = APIRouter()


@auth_router.get("/auth")
async def auth():
    return {"message": "Hello World"}
