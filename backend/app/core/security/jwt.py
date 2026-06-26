from datetime import UTC, datetime, timedelta
from typing import Any

from jose import JWTError, jwt

from app.core.config import settings


def create_access_token(
    subject: str, extra_claims: dict[str, Any] | None = None
) -> str:
    expires_delta = timedelta(minutes=settings.jwt_access_token_expire_minutes)
    now = datetime.now(UTC)
    claims = {
        "sub": subject,
        "iat": now,
        "exp": now + expires_delta,
        "type": "access",
    }
    if extra_claims:
        claims.update(extra_claims)
    return jwt.encode(  # type: ignore[no-any-return]
        claims, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )


def create_refresh_token(subject: str) -> str:
    expires_delta = timedelta(days=settings.jwt_refresh_token_expire_days)
    now = datetime.now(UTC)
    claims = {
        "sub": subject,
        "iat": now,
        "exp": now + expires_delta,
        "type": "refresh",
    }
    return jwt.encode(  # type: ignore[no-any-return]
        claims, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )


def decode_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        return payload  # type: ignore[no-any-return]
    except JWTError as exc:
        raise ValueError("Invalid token") from exc


def verify_token(token: str, expected_type: str = "access") -> dict[str, Any]:
    payload = decode_token(token)
    if payload.get("type") != expected_type:
        raise ValueError(f"Invalid token type: expected {expected_type}")
    return payload
