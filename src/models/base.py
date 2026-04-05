from __future__ import annotations

import re

from sqlalchemy import not_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import as_declarative, declared_attr

from src.models.async_query import AsyncQuery
from src.utils.exceptions import AlreadyExists, ObjectNotFound


@as_declarative()
class Base:
    """Base class for all database entities"""

    @declared_attr
    def __tablename__(cls) -> str:
        """Generate database table name automatically.
        Convert CamelCase class name to snake_case db table name.
        """
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()

    def __repr__(self):
        attrs = []
        for c in self.__table__.columns:
            attrs.append(f"{c.name}={getattr(self, c.name)}")
        return "{}({})".format(c.__class__.__name__, ", ".join(attrs))


class BaseDbModel(Base):
    __abstract__ = True

    @classmethod
    async def create(cls, *, session: AsyncSession, **kwargs) -> BaseDbModel:
        obj = cls(**kwargs)
        session.add(obj)
        await session.flush()
        return obj

    @classmethod
    def query(cls, *, session: AsyncSession, with_deleted: bool = False):
        stmt = select(cls)
        if not with_deleted and hasattr(cls, "is_deleted"):
            stmt = stmt.where(cls.is_deleted.is_(False))
        return AsyncQuery(cls, session, stmt)

    @classmethod
    async def get(
        cls,
        id: int | str,
        *,
        with_deleted: bool = False,
        session: AsyncSession,
    ) -> "BaseDbModel":
        """Get object with soft deletes"""
        stmt = select(cls)
        if not with_deleted and hasattr(cls, "is_deleted"):
            stmt = stmt.where(not_(cls.is_deleted))

        if hasattr(cls, "uuid"):
            stmt = stmt.where(cls.uuid == id)
        else:
            stmt = stmt.where(cls.id == id)

        result = await session.execute(stmt)
        obj = result.scalar_one_or_none()
        if not obj:
            raise ObjectNotFound(cls, id)
        return obj

    @classmethod
    async def update(
        cls,
        id: int | str,
        *,
        session: AsyncSession,
        **kwargs,
    ) -> "BaseDbModel":
        """Update model with new values from kwargs.
        If no new values are given, raise HTTP 409 error.
        """
        get_new_values = False
        obj = await cls.get(id, session=session)
        for k, v in kwargs.items():
            cur_v = getattr(obj, k)
            if cur_v != v:
                setattr(obj, k, v)
                get_new_values = True
        if not get_new_values:
            raise AlreadyExists(cls, id)
        session.add(obj)
        await session.flush()
        return obj

    @classmethod
    async def delete(
        cls,
        id: int | str,
        *,
        session: AsyncSession,
    ) -> None:
        """Soft delete object if possible, else hard delete"""
        obj = await cls.get(id, session=session)
        if hasattr(obj, "is_deleted"):
            obj.is_deleted = True
        else:
            await session.delete(obj)
        await session.flush()
