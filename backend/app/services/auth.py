from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.core.security.password import hash_password, verify_password
from app.models.user import AuthProvider
from app.repositories.user import UserRepository
from app.services.base import ServiceResult


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_repo = UserRepository(session)

    async def register(
        self, email: str, password: str, display_name: str
    ) -> ServiceResult:
        existing = await self.user_repo.get_by_email(email)
        if existing:
            return ServiceResult.error_response("Email already registered", 409)

        user = await self.user_repo.create(
            email=email,
            password_hash=hash_password(password),
            display_name=display_name,
            auth_provider=AuthProvider.EMAIL,
            is_active=True,
        )
        tokens = self._generate_tokens(user.id)
        return ServiceResult.ok(
            {"user": user, **tokens}, status_code=201
        )

    async def login(self, email: str, password: str) -> ServiceResult:
        user = await self.user_repo.get_by_email(email)
        if not user:
            return ServiceResult.error_response("Invalid credentials", 401)
        if not user.password_hash:
            return ServiceResult.error_response(
                "Account uses OAuth. Please sign in with your provider.", 401
            )
        if not verify_password(password, user.password_hash):
            return ServiceResult.error_response("Invalid credentials", 401)
        if not user.is_active:
            return ServiceResult.error_response("Account is deactivated", 403)

        tokens = self._generate_tokens(user.id)
        return ServiceResult.ok({"user": user, **tokens})

    async def refresh_token(self, refresh_token: str) -> ServiceResult:
        try:
            payload = decode_token(refresh_token)
            if payload.get("type") != "refresh":
                return ServiceResult.error_response("Invalid token type", 401)
            user_id = payload.get("sub")
            user = await self.user_repo.get(user_id)
            if not user or not user.is_active:
                return ServiceResult.error_response("User not found or inactive", 401)
            tokens = self._generate_tokens(user.id)
            return ServiceResult.ok(tokens)
        except ValueError:
            return ServiceResult.error_response("Invalid or expired token", 401)

    async def oauth_login(
        self, provider: str, provider_id: str, email: str, display_name: str
    ) -> ServiceResult:
        user = await self.user_repo.get_by_auth_provider(provider, provider_id)
        if not user:
            existing = await self.user_repo.get_by_email(email)
            if existing:
                return ServiceResult.error_response(
                    "Email already registered with a different method", 409
                )
            user = await self.user_repo.create(
                email=email,
                display_name=display_name,
                auth_provider=provider,
                auth_provider_id=provider_id,
                email_verified_at=datetime.now(UTC),
                is_active=True,
            )

        tokens = self._generate_tokens(user.id)
        return ServiceResult.ok({"user": user, **tokens})

    def _generate_tokens(
        self, user_id: str
    ) -> dict:
        return {
            "access_token": create_access_token(user_id),
            "refresh_token": create_refresh_token(user_id),
            "token_type": "bearer",
            "expires_in": 1800,
        }
