from http.client import responses, HTTPException
from unittest.mock import MagicMock, AsyncMock, patch, ANY

import pytest
from fastapi import Response
from src.schemas.user_schema import LoginUser
from src.services.login_service import LoginService


@pytest.mark.asyncio
async def test_user_session_success():

    #Data
    fake_user = MagicMock()
    fake_user.id = 1
    fake_user.email = "mini@gmail.com"
    fake_user.password = "111qwe111"

    #Session
    fake_session = AsyncMock()

    #Data login user
    login_data = LoginUser(email="mini@gmail.com", password="111qwe111")
    response = Response()

    with(
        patch("src.services.login_service.LoginRepo.login_user_repo", new=AsyncMock()) as mock_login_user_repo,
        patch("src.services.login_service.create_access_token") as mock_create_access_token,
        patch("src.services.login_service.create_refresh_token") as mock_create_refresh_token,
        patch("src.services.login_service.RefreshTokenRepo.save_refresh_token", new=AsyncMock()) as mock_save_refresh_token,
    ):
        mock_login_user_repo.return_value = fake_user
        mock_create_access_token.return_value = "fake_access_token"
        mock_create_refresh_token.return_value = "fake_refresh_token"

        result = await LoginService.login_user_service(login_data, response, session=fake_session)

        #Assert
        assert result == {"access_token": "fake_access_token"}
        assert response.headers.get("set-cookie") is not None
        mock_login_user_repo.assert_called_once_with(login_data.email, login_data.password, ANY)
        mock_save_refresh_token.assert_called_once_with(fake_user.id, "fake_refresh_token", ANY)


@pytest.mark.asyncio
async def test_user_not_found():

    login_data = LoginUser(email="mini@gmail.com", password="111qwe111")
    response = Response()

    with patch("src.services.login_service.LoginRepo.login_user_repo", new=AsyncMock) as mock_login_repo:
        mock_login_repo.side_effect = HTTPException(status_code=401, detail="User not found")

        with pytest.raises(HTTPException) as exception:
            await LoginService.login_user_service(login_data, response, session=AsyncMock())
