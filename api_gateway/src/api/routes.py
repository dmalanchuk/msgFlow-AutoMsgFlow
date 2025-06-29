from fastapi import APIRouter, Request
from api_gateway.src.config import settings
from api_gateway.src.utils.proxy_utils import proxy_request

router = APIRouter()

"""proxy to services"""


@router.api_route("/auth{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def auth_proxy(path: str, request: Request):
    url = f"{settings.AUTH_SERVICE_URL}/{path}"
    return await proxy_request(request, url)
