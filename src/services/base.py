from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession


class BaseService:
    model = None

    @classmethod
    async def get_all_rows(
        cls,
        session: AsyncSession
    ):
        query = select(cls.model)
        res = await session.execute(query)
        return res.scalars().all()

    @classmethod
    async def get_all_rows_by_filter(
        cls,
        session: AsyncSession,
        **filter_by
    ):
        query = select(cls.model).filter_by(**filter_by)
        res = await session.execute(query)
        return res.scalars().all()

    @classmethod
    async def get_by_filter(
            cls,
            session: AsyncSession,
            **filter_by
    ):
        query = select(cls.model).filter_by(**filter_by)
        res = await session.execute(query)
        return res.scalar_one_or_none()

    @classmethod
    async def get_by_id(
        cls,
        session: AsyncSession,
        model_id: int
    ):
        query = select(cls.model).filter_by(id=model_id)
        res = await session.execute(query)
        return res.scalar_one_or_none()

    @classmethod
    async def add_row(
        cls,
        session: AsyncSession,
        **data
    ):
        stmt = insert(cls.model).values(data)
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def delete_by_id(
        cls,
        session: AsyncSession,
        model_id: int
    ):
        stmt = delete(cls.model).filter_by(id=model_id)
        await session.execute(stmt)
        await session.commit()
