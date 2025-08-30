from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException

from src.schemas.user_schema import CreateUser
from src.services.reg_service import RegServices


@pytest.mark.asyncio
async def test_register_user_success():
    fake_user = CreateUser(email="mini@gmail.com", username="mini", password="111qwe111")
    fake_session = AsyncMock()

    with patch("src.services.reg_service.RegUser.get_by_email", new=AsyncMock(return_value=None)):
        with patch("src.services.reg_service.RegUser.create_user", new=AsyncMock(return_value={"id": 1, "username": fake_user.username, "email": fake_user.email})):
            user = await RegServices.reg_user_service(fake_user, fake_session)

    assert user["id"] == 1
    assert user["username"] == fake_user.username
    assert user["email"] == fake_user.email


@pytest.mark.asyncio
async def test_reg_user_already_exists():
    fake_user = CreateUser(email="mini@gmail.com", username="mini", password="111qwe111")
    fake_session = AsyncMock()

    with patch("src.services.reg_service.RegUser.get_by_email", new=AsyncMock(return_value={"id": 1, "username": fake_user.username, "email": fake_user.email})):
        with pytest.raises(HTTPException) as exception:
            await RegServices.reg_user_service(fake_user, fake_session)

    assert exception.value.status_code == 409


