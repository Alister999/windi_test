from fastapi import FastAPI
from src.api.v1.router import router as v1_router
import logging

from src.core.database import init_db

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


app = FastAPI(
    title="Messenger",
    description="API messenger",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    debug=True
)

app.include_router(v1_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    await init_db()
    print('DB was initial')