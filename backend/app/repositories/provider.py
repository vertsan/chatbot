from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.provider import AIModel, AIProvider
from app.repositories.base import BaseRepository


class AIProviderRepository(BaseRepository[AIProvider]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, AIProvider)

    async def get_with_models(self, provider_id: str) -> AIProvider | None:
        stmt = (
            select(AIProvider)
            .options(joinedload(AIProvider.models))
            .where(AIProvider.id == provider_id)
        )
        result = await self.session.execute(stmt)
        return result.unique().scalar_one_or_none()

    async def get_default(self) -> AIProvider | None:
        stmt = select(AIProvider).where(
            AIProvider.is_default, AIProvider.is_active
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_active(self) -> Sequence[AIProvider]:
        stmt = select(AIProvider).where(AIProvider.is_active)
        result = await self.session.execute(stmt)
        return result.scalars().all()


class AIModelRepository(BaseRepository[AIModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, AIModel)

    async def get_by_provider(
        self, provider_id: str
    ) -> Sequence[AIModel]:
        stmt = select(AIModel).where(
            AIModel.provider_id == provider_id, AIModel.is_active
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_default_by_provider(
        self, provider_id: str
    ) -> AIModel | None:
        stmt = select(AIModel).where(
            AIModel.provider_id == provider_id,
            AIModel.is_default,
            AIModel.is_active,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
