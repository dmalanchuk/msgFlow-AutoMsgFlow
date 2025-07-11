from fastapi import FastAPI
from src.api import auth_api

app = FastAPI()
app.include_router(auth_api.auth_router, tags=["auth"])
