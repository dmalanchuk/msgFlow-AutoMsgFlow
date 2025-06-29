from fastapi import APIRouter
from api_gateway.src.config import settings
from api_gateway.src.utils.proxy_utils import proxy_request

router = APIRouter()
