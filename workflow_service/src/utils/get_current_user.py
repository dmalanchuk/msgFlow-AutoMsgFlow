from datetime import datetime

import jwt
from jwt import PyJWTError

from src.schemas.token_schema import Token
from src.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8001/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> Token:
    ...
