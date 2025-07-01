from fastapi import FastAPI

from src.api import scenario_api

app = FastAPI()
app.include_router(scenario_api.scenario_router, tags=["scenarios"])
