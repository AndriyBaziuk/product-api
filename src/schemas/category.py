from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase): ...


class CategoryUpdate(CategoryBase): ...


class Category(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
