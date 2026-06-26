from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import (
    JSON,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Entity, SoftDeletable


class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class ConversationStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"


class Chat(Entity):
    __tablename__ = "chats"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False, index=True
    )
    model_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("ai_models.id"), nullable=True
    )
    system_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
    temperature: Mapped[float | None] = mapped_column(Float, default=0.7)
    top_p: Mapped[float | None] = mapped_column(Float, default=1.0)
    max_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    metadata_: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    user: Mapped[User] = relationship()
    model: Mapped[AIModel] = relationship()
    conversations: Mapped[list[Conversation]] = relationship(
        back_populates="chat", cascade="all, delete-orphan"
    )


class Conversation(SoftDeletable):
    __tablename__ = "conversations"

    chat_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("chats.id"), nullable=False, index=True
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[ConversationStatus] = mapped_column(
        default=ConversationStatus.ACTIVE, nullable=False
    )
    model_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("ai_models.id"), nullable=True
    )
    system_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
    temperature: Mapped[float | None] = mapped_column(Float, default=0.7)
    top_p: Mapped[float | None] = mapped_column(Float, default=1.0)
    max_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    token_count: Mapped[int] = mapped_column(Integer, default=0)
    message_count: Mapped[int] = mapped_column(Integer, default=0)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    last_message_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    chat: Mapped[Chat] = relationship(back_populates="conversations")
    user: Mapped[User] = relationship(back_populates="conversations")
    messages: Mapped[list[Message]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="Message.created_at",
    )


class Message(Entity):
    __tablename__ = "messages"

    conversation_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("conversations.id"), nullable=False, index=True
    )
    role: Mapped[MessageRole] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    model_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("ai_models.id"), nullable=True
    )
    provider_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("ai_providers.id"), nullable=True
    )
    tool_calls: Mapped[list | None] = mapped_column(JSON, nullable=True)
    tool_call_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    input_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    output_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    finish_reason: Mapped[str | None] = mapped_column(String(50), nullable=True)
    metadata_: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    is_edited: Mapped[bool] = mapped_column(default=False, nullable=False)
    parent_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("messages.id"), nullable=True
    )

    conversation: Mapped[Conversation] = relationship(back_populates="messages")
    attachments: Mapped[list[Attachment]] = relationship(
        back_populates="message", cascade="all, delete-orphan"
    )


class Attachment(Entity):
    __tablename__ = "attachments"

    message_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("messages.id"), nullable=False, index=True
    )
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(512), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    mime_type: Mapped[str] = mapped_column(String(127), nullable=False)
    storage_type: Mapped[str] = mapped_column(String(50), default="local")
    metadata_: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    message: Mapped[Message] = relationship(back_populates="attachments")
