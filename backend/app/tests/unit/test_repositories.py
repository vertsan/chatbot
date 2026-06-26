from unittest.mock import AsyncMock, MagicMock

import pytest

from app.repositories.user import UserRepository


@pytest.fixture
def mock_session() -> AsyncMock:
    session = AsyncMock()
    session.execute = AsyncMock()
    session.flush = AsyncMock()
    session.add = MagicMock()
    return session


class TestUserRepository:
    def test_create_user(self, mock_session: MagicMock) -> None:
        repo = UserRepository(mock_session)
        repo.create = AsyncMock()
        result = repo.create(
            email="test@example.com",
            display_name="Test User",
            auth_provider="email",
        )
        assert result is not None
