from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api import router as api_router
from core.config import settings
from core.database import session_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await session_manager.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)

app.mount(
    settings.media.url_prefix,
    StaticFiles(directory=settings.media.directory),
    name="media",
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
