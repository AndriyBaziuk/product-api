from abc import ABC, abstractmethod
from typing import TypeVar
from uuid import UUID

from models import Base

PrimaryKeyType = int | str | UUID
Model = TypeVar("Model", bound=Base)


class RepositoryError(Exception): ...


class BaseRepository(ABC):
    @abstractmethod
    def get_all(self, **filter_by) -> list[Model]: ...

    @abstractmethod
    def get(self, pk: PrimaryKeyType) -> Model | None: ...

    @abstractmethod
    def create(self, data: dict) -> Model: ...

    @abstractmethod
    def update(self, pk: PrimaryKeyType, data: dict) -> Model: ...

    @abstractmethod
    def delete(self, pk: PrimaryKeyType) -> None: ...
