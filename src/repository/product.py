from sqlalchemy import exists

from models import Product
from repository.sqlalchemy import SQLAlchemyRepository


class ProductRepository(SQLAlchemyRepository):
    model = Product

    async def exists_by_name(self, name: str) -> bool:
        query = exists(self.model).where(self.model.name == name).select()
        return await self.session.scalar(query)
