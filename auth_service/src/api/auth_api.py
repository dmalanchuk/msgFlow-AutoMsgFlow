from fastapi import APIRouter

auth_router = APIRouter(
    prefix="/auth",
)


@auth_router.post("/")
async def auth():
    return {"message": "Hello World!"}
