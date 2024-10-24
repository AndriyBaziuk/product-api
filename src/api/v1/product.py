from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile

from core.database import DBSessionDep
from repository import ProductRepository
from schemas.product import Product, ProductCreate, ProductUpdate
from service.product import ProductService

router = APIRouter(tags=["Products"])


def get_product_service(session: DBSessionDep):
    repository = ProductRepository(session=session)
    return ProductService(repository=repository)


ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]


@router.get("", response_model=list[Product])
async def get_product_list(product_service: ProductServiceDep):
    return await product_service.get_all()


@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: int, product_service: ProductServiceDep):
    return await product_service.get(_id=product_id)


@router.post("", response_model=Product)
async def create_product(product: ProductCreate, product_service: ProductServiceDep):
    return await product_service.create(product=product)


@router.patch("/{product_id}", response_model=Product)
async def update_product(
    product_id: int, product: ProductUpdate, product_service: ProductServiceDep
):
    return await product_service.update(_id=product_id, product=product)


@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: int, product_service: ProductServiceDep):
    return await product_service.delete(_id=product_id)


@router.post("/{product_id}/upload-image", status_code=200, response_model=Product)
async def upload_product_image(
    product_id: int, image: UploadFile, product_service: ProductServiceDep
):
    return await product_service.upload_image(_id=product_id, image=image)
