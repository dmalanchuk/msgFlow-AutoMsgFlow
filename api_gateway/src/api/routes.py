from typing import Optional

from fastapi import APIRouter, Request, Body
from src.config import settings
from src.utils.proxy_utils import proxy_request

router = APIRouter()

"""proxy to services"""


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

#integrations
@router.api_route("/integration{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def auth_proxy(path: str, request: Request):
    url = f"{settings.INTERACTION_SERVICE_URL}/{path}"
    return await proxy_request(request, url)