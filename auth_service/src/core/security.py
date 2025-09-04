from concurrent.futures.thread import ThreadPoolExecutor
import asyncio
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
executor = ThreadPoolExecutor()


async def hash_password(password: str) -> str:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, pwd_context.hash, password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)