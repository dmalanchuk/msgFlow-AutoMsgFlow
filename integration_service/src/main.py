from fastapi import FastAPI
from src.routes.router import router

app = FastAPI(title="Integration Service", )
app.include_router(router)
