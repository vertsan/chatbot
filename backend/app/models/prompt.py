from sqlalchemy import JSON, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import SoftDeletable


class PromptTemplate(SoftDeletable):
    __tablename__ = "prompt_templates"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    user_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=True, index=True
    )
    organization_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("organizations.id"), nullable=True, index=True
    )
    is_global: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_system: Mapped[bool] = mapped_column(default=False, nullable=False)
    variables: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    version: Mapped[int] = mapped_column(default=1, nullable=False)
    metadata_: Mapped[dict | None] = mapped_column(JSON, nullable=True)
