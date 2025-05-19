import os
import pytest
import pytest_asyncio
from httpx import AsyncClient
from httpx import ASGITransport
from sqlalchemy import text
from src.main import app
from src.core.database import init_db, get_db
from src.models.general import Base


@pytest.fixture(scope="session", autouse=True)
def set_test_env():
    os.environ["IS_TEST"] = "1"


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    await init_db()


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture(autouse=True)
async def clean_db():
    yield

    async for session in get_db():
        result = await session.execute(text("SELECT current_database()"))
        db_name = result.scalar()
        if "test_db" not in db_name:
            raise RuntimeError(f"❌ CLEAN_DB попытался очистить не тестовую базу: {db_name}")

        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()
        break
