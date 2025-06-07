from contextlib import asynccontextmanager
from typing import TypeVar, Generic, Type

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select, delete, update
from sqlalchemy.orm import joinedload

from app.db.base_class import Base
from app.db.initial_models import Route
from app.db.session import AsyncSessionLocal
from fastapi_pagination.ext.sqlalchemy import paginate

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase:
    def __init__(self, model: Type[ModelType], db: AsyncSessionLocal = None):
        self.model = model
        self.db = db or AsyncSessionLocal()

    @asynccontextmanager
    async def get_session(self):
        try:
            yield self.db
        finally:
            await self.db.close()

    async def create(self, data: CreateSchemaType):
        async with self.get_session() as session:
            db_instance = self.model(**data.model_dump())
            session.add(db_instance)
            await session.flush()
            await session.commit()
            return db_instance

    async def get(self, id_: int):
        async with self.get_session() as session:
            result = await session.execute(select(self.model).filter(self.model.id == id_))
            return result.scalar_one_or_none()

    async def update(self, id_: int, data: UpdateSchemaType):
        async with self.get_session() as session:
            stmt = (
                update(self.model)
                .where(self.model.id == id_)
                .values(**data.model_dump())
                .execution_options(synchronize_session="fetch")
            )
            await session.execute(stmt)
            await session.commit()
            result = await session.execute(select(self.model).filter(self.model.id == id_))
            return result.scalar_one_or_none()

    async def remove(self, id_: int):
        async with self.get_session() as session:
            query = select(self.model).where(self.model.id == id_)
            result = await session.execute(query)
            existing_route = result.scalars().first()
            if not existing_route:
                raise HTTPException(status_code=404, detail="Route not found")

            await session.delete(existing_route)
            await session.commit()

    async def get_all(self, in_pages: bool = True) -> list[ModelType]:
        async with self.get_session() as session:
            query = select(self.model)

            if self.model == Route:
                query = query.options(joinedload(Route.schedules))

            if in_pages:
                result = await paginate(session, query)
            else:
                result = await session.execute(query)
                result = result.scalars().all()

            return result



