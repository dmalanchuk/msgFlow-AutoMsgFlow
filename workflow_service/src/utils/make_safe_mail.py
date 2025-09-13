import hashlib
from pydantic import EmailStr


def make_chat_key(email: EmailStr) -> str:
    return f"chat:{hashlib.md5(str(email).encode()).hexdigest()}:updates"
