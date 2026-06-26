from unittest.mock import AsyncMock, MagicMock

import pytest

from app.services.auth import AuthService


@pytest.fixture
def mock_session() -> AsyncMock:
    return AsyncMock()


class TestAuthService:
    async def test_register_success(self, mock_session: MagicMock) -> None:
        service = AuthService(mock_session)
        service.user_repo = AsyncMock()
        service.user_repo.get_by_email = AsyncMock(return_value=None)
        service.user_repo.create = AsyncMock(
            return_value=MagicMock(id="new-user-id")
        )

        result = await service.register(
            email="test@example.com",
            password="password123",
            display_name="Test User",
        )
        assert result.success
        assert result.status_code == 201

    async def test_register_duplicate(self, mock_session: MagicMock) -> None:
        service = AuthService(mock_session)
        service.user_repo = AsyncMock()
        service.user_repo.get_by_email = AsyncMock(
            return_value=MagicMock()
        )

        result = await service.register(
            email="existing@example.com",
            password="password123",
            display_name="Test",
        )
        assert not result.success
        assert result.status_code == 409

    async def test_login_invalid(self, mock_session: MagicMock) -> None:
        service = AuthService(mock_session)
        service.user_repo = AsyncMock()
        service.user_repo.get_by_email = AsyncMock(return_value=None)

        result = await service.login(
            email="nonexistent@example.com", password="password123"
        )
        assert not result.success
        assert result.status_code == 401
