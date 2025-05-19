from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.api.v1.router import router as v1_router
import logging
from src.core.database import init_db
from src.core.loging_config import setup_logging


setup_logging()
logger = logging.getLogger("MainApp")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    logger.info("DB was init")
    yield

app = FastAPI(
    title="Messenger",
    description="API messenger",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.include_router(v1_router, prefix="/api")
