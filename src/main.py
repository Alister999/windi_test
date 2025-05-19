from fastapi import FastAPI
from src.api.v1.router import router as v1_router
import logging

from src.core.database import init_db #, init_config
from src.core.loging_config import setup_logging

setup_logging()

logger = logging.getLogger("MainApp")


app = FastAPI(
    title="Messenger",
    description="API messenger",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    debug=True
)

app.include_router(v1_router, prefix="/api")


# @app.on_event("startup")
# async def startup_event():
#     await init_db()
#     logger.info("DB was init")

@app.on_event("startup")
async def startup_event():
    # init_config()  # обязательно!
    await init_db()
    logger.info("DB was init")
