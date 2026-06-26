from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from sqlalchemy import Select, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from app.database.base import Entity

T = TypeVar("T", bound=Entity)


class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: type[T]) -> None:
        self.session = session
        self.model = model

    async def create(self, **kwargs: Any) -> T:
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        return instance

    async def get(self, id: str) -> T | None:
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_many(
        self,
        skip: int = 0,
        limit: int = 50,
        filters: dict[str, Any] | None = None,
        order_by: str | None = None,
        descending: bool = False,
    ) -> tuple[Sequence[T], int]:
        stmt = select(self.model)
        count_stmt = select(func.count()).select_from(self.model)

        if filters:
            for field, value in filters.items():
                column = getattr(self.model, field, None)
                if column is not None:
                    stmt = stmt.where(column == value)
                    count_stmt = count_stmt.where(column == value)

        count_result = await self.session.execute(count_stmt)
        total = count_result.scalar() or 0

        if order_by:
            column = getattr(self.model, order_by, None)
            if column is not None:
                stmt = stmt.order_by(column.desc() if descending else column)

        stmt = stmt.offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        items = result.scalars().all()
        return items, total

    async def update(self, id: str, **kwargs: Any) -> T | None:
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**kwargs)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.scalar_one_or_none()

    async def delete(self, id: str, soft: bool = True) -> bool:
        if soft and hasattr(self.model, "deleted_at"):
            stmt = (
                update(self.model)
                .where(self.model.id == id)
                .values(deleted_at=func.now(), is_deleted=True)
            )
        else:
            stmt = delete(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount > 0

    async def exists(self, **filters: Any) -> bool:
        stmt = select(self.model)
        for field, value in filters.items():
            column = getattr(self.model, field, None)
            if column is not None:
                stmt = stmt.where(column == value)
        stmt = stmt.limit(1)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    def _apply_filters(
        self, stmt: Select, filters: dict[str, Any]
    ) -> Select:
        for field, value in filters.items():
            column = getattr(self.model, field, None)
            if column is not None:
                stmt = stmt.where(column == value)
        return stmt
