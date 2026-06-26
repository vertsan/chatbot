from datetime import datetime

from pydantic import BaseModel, Field


class KnowledgeBaseCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    embedding_model: str = "text-embedding-3-small"
    chunk_size: int = Field(1000, ge=100, le=10000)
    chunk_overlap: int = Field(200, ge=0, le=1000)


class KnowledgeBaseUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    is_active: bool | None = None


class KnowledgeBaseResponse(BaseModel):
    id: str
    name: str
    description: str | None = None
    user_id: str
    organization_id: str | None = None
    embedding_model: str
    chunk_size: int
    chunk_overlap: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DocumentUploadResponse(BaseModel):
    id: str
    file_name: str
    file_size: int
    mime_type: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentResponse(BaseModel):
    id: str
    knowledge_base_id: str
    file_name: str
    file_size: int
    mime_type: str
    document_type: str
    status: str
    chunk_count: int
    error_message: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RAGQuery(BaseModel):
    query: str = Field(..., min_length=1)
    knowledge_base_id: str
    top_k: int = Field(5, ge=1, le=50)
    similarity_threshold: float = Field(0.7, ge=0.0, le=1.0)


class RAGResult(BaseModel):
    chunks: list[dict]
    query: str
    total_chunks: int
