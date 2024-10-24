from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from repository.base import BaseRepository, Model, PrimaryKeyType, RepositoryError


class SQLAlchemyRepository(BaseRepository):
    model: type[Model] = None

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @property
    def model_name(self) -> str:
        return self.model.__class__.__name__

    async def get_all(self, **filter_by) -> list[Model]:
        try:
            query = select(self.model).filter_by(**filter_by)
            result = await self.session.execute(query)
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise RepositoryError(f"Failed to find all {self.model_name}: {e}")

    async def get(self, pk: PrimaryKeyType) -> Model:
        try:
            return await self.session.get(self.model, pk)
        except SQLAlchemyError as e:
            raise RepositoryError(f"Failed to find {self.model_name} by id {pk}: {e}")

    async def create(self, data: dict) -> Model:
        try:
            entity = self.model(**data)
            self.session.add(entity)
            await self.session.commit()
            await self.session.refresh(entity)
            return entity
        except SQLAlchemyError as e:
            raise RepositoryError(f"Failed to create {self.model_name}: {e}")

    async def update(self, pk: PrimaryKeyType, data: dict) -> Model:
        try:
            entity = await self.session.get(self.model, pk)
            for key, value in data.items():
                setattr(entity, key, value)
            await self.session.commit()
            return entity
        except SQLAlchemyError as e:
            raise RepositoryError(f"Failed to update {self.model_name} by id {pk}: {e}")

    async def delete(self, pk: PrimaryKeyType) -> None:
        try:
            entity = await self.session.get(self.model, pk)
            if entity is not None:
                await self.session.delete(entity)
                await self.session.commit()
        except SQLAlchemyError as e:
            raise RepositoryError(f"Failed to delete {self.model_name} by id {pk}: {e}")
