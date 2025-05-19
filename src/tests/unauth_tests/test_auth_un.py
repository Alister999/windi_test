import pytest
from httpx import AsyncClient


pytestmark = pytest.mark.asyncio


async def test_get_users_without_auth(client: AsyncClient):
    response = await client.get("/api/v1/user")
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }


async def test_delete_users_without_auth(client: AsyncClient):
    response = await client.delete("/api/v1/delete_user/1")
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }


async def test_get_user_without_auth(client: AsyncClient):
    response = await client.get("/api/v1/user/1")
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }


async def test_put_user_without_auth(client: AsyncClient):
    response = await client.put("/api/v1/user/1")
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }