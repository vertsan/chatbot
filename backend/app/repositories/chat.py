from collections.abc import Sequence

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.chat import Chat, Conversation, Message
from app.repositories.base import BaseRepository


class ChatRepository(BaseRepository[Chat]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Chat)

    async def get_with_conversations(self, chat_id: str) -> Chat | None:
        stmt = (
            select(Chat)
            .options(joinedload(Chat.conversations))
            .where(Chat.id == chat_id)
        )
        result = await self.session.execute(stmt)
        return result.unique().scalar_one_or_none()


class ConversationRepository(BaseRepository[Conversation]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Conversation)

    async def get_by_user(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 50,
        search: str | None = None,
        status: str | None = None,
    ) -> tuple[Sequence[Conversation], int]:
        stmt = select(Conversation).where(
            Conversation.user_id == user_id,
            not Conversation.is_deleted,
        )
        count_stmt = select(func.count()).select_from(Conversation).where(
            Conversation.user_id == user_id,
            not Conversation.is_deleted,
        )

        if search:
            stmt = stmt.where(Conversation.title.ilike(f"%{search}%"))
            count_stmt = count_stmt.where(Conversation.title.ilike(f"%{search}%"))

        if status:
            stmt = stmt.where(Conversation.status == status)
            count_stmt = count_stmt.where(Conversation.status == status)

        count_result = await self.session.execute(count_stmt)
        total = count_result.scalar() or 0

        stmt = stmt.order_by(Conversation.last_message_at.desc().nullslast())
        stmt = stmt.offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        items = result.scalars().all()
        return items, total

    async def update_message_count(self, conversation_id: str) -> None:
        from app.models.chat import Message

        subq = (
            select(func.count())
            .select_from(Message)
            .where(Message.conversation_id == conversation_id)
            .scalar_subquery()
        )
        stmt = (
            update(Conversation)
            .where(Conversation.id == conversation_id)
            .values(message_count=subq)
        )
        await self.session.execute(stmt)
        await self.session.flush()


class MessageRepository(BaseRepository[Message]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Message)

    async def get_by_conversation(
        self, conversation_id: str, skip: int = 0, limit: int = 200
    ) -> tuple[Sequence[Message], int]:
        stmt = select(Message).where(
            Message.conversation_id == conversation_id
        )
        count_stmt = (
            select(func.count())
            .select_from(Message)
            .where(Message.conversation_id == conversation_id)
        )
        count_result = await self.session.execute(count_stmt)
        total = count_result.scalar() or 0

        stmt = stmt.order_by(Message.created_at.asc())
        stmt = stmt.offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        items = result.scalars().all()
        return items, total
