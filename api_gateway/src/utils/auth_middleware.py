from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError

from src.config import settings

SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        open_paths = [
            "/docs",
            "/openapi.json",
            "/auth/login",
            "/auth/register",
        ]
        if any(path.startswith(open_path) for open_path in open_paths):
            return await call_next(request)

        token = request.cookies.get("refresh_token")
        if not token:
            raise HTTPException(status_code=401, detail="Token cookie missing")

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_email = payload.get("sub")
            if not user_email:
                raise HTTPException(status_code=401, detail="Email not found in token")

            request.state.user_email = user_email
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        return await call_next(request)
