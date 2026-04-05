from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class AsyncQuery:
    def __init__(self, model, session: AsyncSession, stmt=None):
        self.model = model
        self.session = session
        self.stmt = stmt if stmt is not None else select(model)

    def filter(self, *conditions):
        new_stmt = self.stmt.where(*conditions)
        return AsyncQuery(self.model, self.session, new_stmt)

    async def one_or_none(self):
        result = await self.session.execute(self.stmt)
        return result.scalar_one_or_none()

    async def all(self):
        result = await self.session.execute(self.stmt)
        return result.scalars().all()

    async def first(self):
        result = await self.session.execute(self.stmt)
        return result.scalars().first()
