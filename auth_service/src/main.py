from fastapi import FastAPI
from auth_service.src.api import auth_api

app = FastAPI()
app.include_router(auth_api.auth_router)
