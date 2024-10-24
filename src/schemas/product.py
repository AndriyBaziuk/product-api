from pydantic import BaseModel, ConfigDict

from .category import Category


class ProductBase(BaseModel):
    name: str
    description: str
    price: float


class ProductCreate(ProductBase):
    category_id: int


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    category_id: int | None = None


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    image_url: str | None
    category: Category
