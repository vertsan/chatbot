from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class MessageRole(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class ChatCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    model_id: str | None = None
    system_prompt: str | None = None
    temperature: float | None = Field(None, ge=0.0, le=2.0)
    top_p: float | None = Field(None, ge=0.0, le=1.0)
    max_tokens: int | None = Field(None, ge=1, le=131072)


class ChatUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    model_id: str | None = None
    system_prompt: str | None = None
    temperature: float | None = Field(None, ge=0.0, le=2.0)
    top_p: float | None = Field(None, ge=0.0, le=1.0)
    max_tokens: int | None = Field(None, ge=1, le=131072)


class ChatResponse(BaseModel):
    id: str
    title: str
    model_id: str | None = None
    system_prompt: str | None = None
    temperature: float | None = None
    top_p: float | None = None
    max_tokens: int | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ConversationCreate(BaseModel):
    chat_id: str
    title: str = Field(..., min_length=1, max_length=255)
    model_id: str | None = None
    system_prompt: str | None = None
    temperature: float | None = Field(None, ge=0.0, le=2.0)
    top_p: float | None = Field(None, ge=0.0, le=1.0)
    max_tokens: int | None = Field(None, ge=1, le=131072)


class ConversationUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    status: str | None = None


class ConversationResponse(BaseModel):
    id: str
    chat_id: str
    user_id: str
    title: str
    status: str
    model_id: str | None = None
    system_prompt: str | None = None
    temperature: float | None = None
    top_p: float | None = None
    max_tokens: int | None = None
    token_count: int = 0
    message_count: int = 0
    summary: str | None = None
    last_message_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ConversationListResponse(BaseModel):
    items: list[ConversationResponse]
    total: int
    page: int
    page_size: int


class MessageSend(BaseModel):
    content: str = Field(..., min_length=1)
    role: MessageRole = MessageRole.USER
    parent_id: str | None = None
    attachments: list[str] | None = None


class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str
    model_id: str | None = None
    provider_id: str | None = None
    tool_calls: list | None = None
    tool_call_id: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None
    latency_ms: int | None = None
    finish_reason: str | None = None
    created_at: datetime
    parent_id: str | None = None

    class Config:
        from_attributes = True


class StreamChunk(BaseModel):
    content: str
    done: bool = False
    finish_reason: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
