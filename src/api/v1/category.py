from typing import Annotated

from fastapi import APIRouter, Depends

from core.database import DBSessionDep
from repository import CategoryRepository
from schemas.category import Category, CategoryCreate, CategoryUpdate
from service.category import CategoryService

router = APIRouter(tags=["Categories"])


def get_category_service(session: DBSessionDep) -> CategoryService:
    repository = CategoryRepository(session=session)
    return CategoryService(repository=repository)


CategoryServiceDep = Annotated[CategoryService, Depends(get_category_service)]


@router.get("", status_code=200, response_model=list[Category])
async def get_category_list(category_service: CategoryServiceDep):
    return await category_service.get_all()


@router.get("/{category_id}", status_code=200, response_model=Category)
async def get_category(category_id: int, category_service: CategoryServiceDep):
    return await category_service.get(_id=category_id)


@router.post("", status_code=201, response_model=Category)
async def create_category(
    category: CategoryCreate, category_service: CategoryServiceDep
):
    return await category_service.create(category=category)


@router.patch("/{category_id}", status_code=200, response_model=Category)
async def update_category(
    category_id: int, category: CategoryUpdate, category_service: CategoryServiceDep
):
    return await category_service.update(_id=category_id, category=category)


@router.delete("/{category_id}", status_code=204)
async def delete_category(category_id: int, category_service: CategoryServiceDep):
    return await category_service.delete(_id=category_id)
