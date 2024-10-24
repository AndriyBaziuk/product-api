from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base

if TYPE_CHECKING:
    from .category import Category


class Product(Base):
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(default="")
    price: Mapped[float] = mapped_column(default=0.0)
    image_url: Mapped[str] = mapped_column(nullable=True, default=None)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    category: Mapped["Category"] = relationship(
        back_populates="products",
        lazy="selectin",
    )
