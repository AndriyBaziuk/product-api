import uuid
from pathlib import Path

import aiofiles
from fastapi import HTTPException, UploadFile

from core.config import settings
from models import Product
from repository import ProductRepository
from schemas.product import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, repository: ProductRepository) -> None:
        self.repository = repository

    async def get_all(self) -> list[Product]:
        return await self.repository.get_all()

    async def get(self, _id: int) -> Product:
        if not (product := await self.repository.get(pk=_id)):
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    async def create(self, product: ProductCreate) -> Product:
        if await self.repository.exists_by_name(name=product.name):
            raise HTTPException(
                status_code=400,
                detail="Product with such name already exist",
            )
        data = product.model_dump()
        return await self.repository.create(data=data)

    async def update(self, _id: int, product: ProductUpdate) -> Product:
        if not await self.repository.get(pk=_id):
            raise HTTPException(status_code=404, detail="Product not found")
        data = product.model_dump(exclude_none=True)
        return await self.repository.update(pk=_id, data=data)

    async def delete(self, _id: int) -> None:
        if not (product := await self.repository.get(pk=_id)):
            raise HTTPException(status_code=404, detail="Product not found")
        self.__delete_image(filepath=product.image_url)
        return await self.repository.delete(pk=_id)

    async def upload_image(self, _id: int, image: UploadFile) -> Product:
        product = await self.repository.get(pk=_id)
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        if product.image_url is not None:
            self.__delete_image(filepath=product.image_url)
        filepath = await self.__save_image(image=image)
        return await self.repository.update(pk=_id, data={"image_url": filepath})

    async def __save_image(self, image: UploadFile) -> str:
        media_directory = Path(settings.media.directory)
        if not media_directory.exists():
            media_directory.mkdir()

        extension = Path(image.filename).suffix
        filename = f"{uuid.uuid4().hex}{extension}"
        filepath = media_directory / filename
        content = await image.read()

        async with aiofiles.open(filepath, "wb") as f:
            await f.write(content)

        return str(filepath)

    def __delete_image(self, filepath: str) -> None:
        Path(filepath).unlink()
