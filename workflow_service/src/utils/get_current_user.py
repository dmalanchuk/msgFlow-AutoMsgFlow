from datetime import datetime

import jwt
from jwt import PyJWTError

from src.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
