from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email, User.is_deleted == False)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_auth_provider(
        self, provider: str, provider_id: str
    ) -> User | None:
        stmt = select(User).where(
            User.auth_provider == provider,
            User.auth_provider_id == provider_id,
            User.is_deleted == False,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def mark_email_verified(self, user_id: str) -> None:
        from datetime import datetime, timezone

        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(email_verified_at=datetime.now(timezone.utc))
        )
        await self.session.execute(stmt)
        await self.session.flush()
