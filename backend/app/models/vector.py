from sqlalchemy import JSON, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Entity


class VectorIndex(Entity):
    __tablename__ = "vector_indices"

    document_chunk_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("document_chunks.id"), nullable=True, index=True
    )
    vector_store_type: Mapped[str] = mapped_column(String(50), nullable=False)
    vector_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    dimensions: Mapped[int] = mapped_column(Integer, nullable=False)
    model_name: Mapped[str] = mapped_column(String(255), nullable=False)
    metadata: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    __table_args__ = (
        {"extend_existing": True},
    )
