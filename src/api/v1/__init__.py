from fastapi import APIRouter

from core.config import settings

from .category import router as category_router
from .product import router as product_router

router = APIRouter(prefix=settings.api.v1.prefix)

router.include_router(category_router, prefix=settings.api.v1.category)
router.include_router(product_router, prefix=settings.api.v1.products)
