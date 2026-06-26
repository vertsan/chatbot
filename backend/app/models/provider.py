from enum import Enum

from sqlalchemy import Boolean, Float, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Entity


class ProviderType(str, Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    AZURE_OPENAI = "azure_openai"
    HUGGINGFACE = "huggingface"
    GROQ = "groq"
    DEEPSEEK = "deepseek"
    LM_STUDIO = "lm_studio"
    VLLM = "vllm"
    CUSTOM = "custom"


class AIProvider(Entity):
    __tablename__ = "ai_providers"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    provider_type: Mapped[ProviderType] = mapped_column(nullable=False)
    api_base_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    api_key: Mapped[str | None] = mapped_column(String(512), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_default: Mapped[bool] = mapped_column(default=False, nullable=False)
    config: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    rate_limit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    max_connections: Mapped[int | None] = mapped_column(Integer, nullable=True)
    metadata: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    models: Mapped[list["AIModel"]] = relationship(
        back_populates="provider", cascade="all, delete-orphan"
    )


class AIModel(Entity):
    __tablename__ = "ai_models"

    provider_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("ai_providers.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    model_id: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    max_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    context_length: Mapped[int | None] = mapped_column(Integer, nullable=True)
    supports_streaming: Mapped[bool] = mapped_column(default=True, nullable=False)
    supports_tools: Mapped[bool] = mapped_column(default=False, nullable=False)
    supports_vision: Mapped[bool] = mapped_column(default=False, nullable=False)
    supports_embeddings: Mapped[bool] = mapped_column(default=False, nullable=False)
    supports_json_mode: Mapped[bool] = mapped_column(default=False, nullable=False)
    input_price_per_1k: Mapped[float | None] = mapped_column(Float, nullable=True)
    output_price_per_1k: Mapped[float | None] = mapped_column(Float, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_default: Mapped[bool] = mapped_column(default=False, nullable=False)
    metadata: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    provider: Mapped["AIProvider"] = relationship(back_populates="models")
