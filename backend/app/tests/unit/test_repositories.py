import pytest
from unittest.mock import AsyncMock, MagicMock

from app.repositories.user import UserRepository
from app.repositories.chat import ChatRepository, ConversationRepository


@pytest.fixture
def mock_session():
    session = AsyncMock()
    session.execute = AsyncMock()
    session.flush = AsyncMock()
    session.add = MagicMock()
    return session


class TestUserRepository:
    def test_create_user(self, mock_session):
        repo = UserRepository(mock_session)
        repo.create = AsyncMock()
        result = repo.create(
            email="test@example.com",
            display_name="Test User",
            auth_provider="email",
        )
        assert result is not None
