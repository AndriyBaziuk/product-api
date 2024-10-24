from fastapi import HTTPException

from models import Category
from repository import CategoryRepository
from schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    def __init__(self, repository: CategoryRepository) -> None:
        self.repository = repository

    async def get_all(self) -> list[Category]:
        return await self.repository.get_all()

    async def get(self, _id: int) -> Category:
        if not (category := await self.repository.get(pk=_id)):
            raise HTTPException(status_code=404, detail="Product not found")
        return category

    async def create(self, category: CategoryCreate) -> Category:
        if await self.repository.exists_by_name(name=category.name):
            raise HTTPException(
                status_code=400,
                detail="Category with such name already exist",
            )
        data = category.model_dump()
        return await self.repository.create(data=data)

    async def update(self, _id: int, category: CategoryUpdate) -> Category:
        if not await self.repository.get(pk=_id):
            raise HTTPException(status_code=404, detail="Product not found")
        data = category.model_dump(exclude_none=True)
        return await self.repository.update(pk=_id, data=data)

    async def delete(self, _id: int) -> None:
        if not await self.repository.get(pk=_id):
            raise HTTPException(status_code=404, detail="Product not found")
        return await self.repository.delete(pk=_id)
