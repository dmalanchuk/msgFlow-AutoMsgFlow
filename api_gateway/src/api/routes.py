from typing import Optional

from fastapi import APIRouter, Request, Body
from src.config import settings
from src.utils.proxy_utils import proxy_request

router = APIRouter()

"""
    auth service service have one get requests and three post request
    get request: /profile
    post request: /login, /register, /logout
"""


@router.get("/auth/{path:path}")
async def auth_proxy_get(path: str, request: Request):
    url = f"{settings.AUTH_SERVICE_URL}/auth/{path}"
    return await proxy_request(request, url)


@router.post("/auth/{path:path}")
async def auth_proxy_with_body(
        path: str,
        request: Request,
        json_body: Optional[dict] = Body(default=None)
):
    url = f"{settings.AUTH_SERVICE_URL}/auth/{path}"
    return await proxy_request(request, url)


"""
    workflow service have two get requests and one post request
    get request: /metadata/actions, /metadata/conditions
    post request: /create
"""


@router.get("/scenarios/{path:path}")
async def scenarios_proxy_get(path: str, request: Request):
    url = f"{settings.WORKFLOW_SERVICE_URL}/scenarios/{path}"
    return await proxy_request(request, url)


@router.post("/scenarios/{path:path}")
async def scenarios_proxy_post(
        path: str,
        request: Request,
        json_body: Optional[dict] = Body(default=None)
):
    url = f"{settings.WORKFLOW_SERVICE_URL}/scenarios/{path}"
    return await proxy_request(request, url)
