from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.knowledge import Document, KnowledgeBase
from app.repositories.base import BaseRepository


class KnowledgeBaseRepository(BaseRepository[KnowledgeBase]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, KnowledgeBase)

    async def get_by_user(
        self, user_id: str, skip: int = 0, limit: int = 50
    ) -> tuple[Sequence[KnowledgeBase], int]:
        stmt = select(KnowledgeBase).where(
            KnowledgeBase.user_id == user_id, not KnowledgeBase.is_deleted
        )
        count_stmt = (
            select(func.count())
            .select_from(KnowledgeBase)
            .where(
                KnowledgeBase.user_id == user_id,
                not KnowledgeBase.is_deleted,
            )
        )
        count_result = await self.session.execute(count_stmt)
        total = count_result.scalar() or 0
        stmt = stmt.offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        items = result.scalars().all()
        return items, total


class DocumentRepository(BaseRepository[Document]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Document)

    async def get_by_knowledge_base(
        self, kb_id: str, skip: int = 0, limit: int = 50
    ) -> tuple[Sequence[Document], int]:
        stmt = select(Document).where(
            Document.knowledge_base_id == kb_id, not Document.is_deleted
        )
        count_stmt = (
            select(func.count())
            .select_from(Document)
            .where(
                Document.knowledge_base_id == kb_id,
                not Document.is_deleted,
            )
        )
        count_result = await self.session.execute(count_stmt)
        total = count_result.scalar() or 0
        stmt = stmt.offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        items = result.scalars().all()
        return items, total

    async def get_with_chunks(self, document_id: str) -> Document | None:
        stmt = (
            select(Document)
            .options(joinedload(Document.chunks))
            .where(Document.id == document_id)
        )
        result = await self.session.execute(stmt)
        return result.unique().scalar_one_or_none()
