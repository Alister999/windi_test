from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import router as v1_router
# from app.core.config import settings
# from app.core.database import init_db, db_config
import logging

from app.core.database import init_db

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


app = FastAPI(
    title="Messenger",
    description="API messenger",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(v1_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    await init_db()
    print('DB was initial')