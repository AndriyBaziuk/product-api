from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base

if TYPE_CHECKING:
    from .product import Product


class Category(Base):
    name: Mapped[str] = mapped_column(unique=True)
    products: Mapped[list["Product"]] = relationship(
        back_populates="category",
        lazy="selectin",
    )
