import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.core.security.jwt import create_access_token, create_refresh_token, decode_token
from app.core.security.password import hash_password, verify_password


class TestPasswordHashing:
    def test_hash_password(self):
        password = "test_password_123"
        hashed = hash_password(password)
        assert hashed != password
        assert verify_password(password, hashed)

    def test_verify_wrong_password(self):
        hashed = hash_password("correct_password")
        assert not verify_password("wrong_password", hashed)


class TestJWT:
    def test_create_access_token(self):
        token = create_access_token("user-123")
        assert token is not None
        payload = decode_token(token)
        assert payload["sub"] == "user-123"
        assert payload["type"] == "access"

    def test_create_refresh_token(self):
        token = create_refresh_token("user-123")
        assert token is not None
        payload = decode_token(token)
        assert payload["sub"] == "user-123"
        assert payload["type"] == "refresh"

    def test_invalid_token(self):
        with pytest.raises(ValueError, match="Invalid token"):
            decode_token("invalid.token.here")
