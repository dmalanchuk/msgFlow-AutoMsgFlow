from fastapi import FastAPI

from src.api.scenario_api import router

app = FastAPI()
app.include_router(router, tags=["scenarios"])
