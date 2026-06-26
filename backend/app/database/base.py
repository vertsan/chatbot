from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import DateTime, String, event
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, registry


class Base(DeclarativeBase):
    registry = registry(
        type_annotation_map={
            datetime: DateTime(timezone=True),
        }
    )


class Entity(Base):
    __abstract__ = True

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )


class SoftDeletable(Entity):
    __abstract__ = True

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None, nullable=True
    )
    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False)


@event.listens_for(SoftDeletable, "load", propagate=True)
def receive_load(target: SoftDeletable, _context: object) -> None:
    target.is_deleted = target.deleted_at is not None
