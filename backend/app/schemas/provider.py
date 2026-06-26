from datetime import datetime

from pydantic import BaseModel, Field


class AIProviderCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    provider_type: str
    api_base_url: str | None = None
    api_key: str | None = None
    is_default: bool = False
    config: dict | None = None


class AIProviderUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    api_base_url: str | None = None
    api_key: str | None = None
    is_active: bool | None = None
    is_default: bool | None = None
    config: dict | None = None


class AIProviderResponse(BaseModel):
    id: str
    name: str
    provider_type: str
    api_base_url: str | None = None
    is_active: bool
    is_default: bool
    config: dict | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AIModelCreate(BaseModel):
    provider_id: str
    name: str = Field(..., min_length=1, max_length=255)
    model_id: str = Field(..., min_length=1, max_length=255)
    version: str | None = None
    description: str | None = None
    max_tokens: int | None = None
    context_length: int | None = None
    supports_streaming: bool = True
    supports_tools: bool = False
    supports_vision: bool = False
    supports_embeddings: bool = False
    supports_json_mode: bool = False
    is_default: bool = False


class AIModelResponse(BaseModel):
    id: str
    provider_id: str
    name: str
    model_id: str
    version: str | None = None
    description: str | None = None
    max_tokens: int | None = None
    context_length: int | None = None
    supports_streaming: bool
    supports_tools: bool
    supports_vision: bool
    supports_embeddings: bool
    supports_json_mode: bool
    input_price_per_1k: float | None = None
    output_price_per_1k: float | None = None
    is_active: bool
    is_default: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
