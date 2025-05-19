import pytest
from httpx import AsyncClient


pytestmark = pytest.mark.asyncio


async def test_post_group_without_auth(client: AsyncClient):
    response = await client.post("/api/v1/group")
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }


async def test_delete_group_without_auth(client: AsyncClient):
    response = await client.delete("/api/v1/group/1")
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }


async def test_get_groups_without_auth(client: AsyncClient):
    response = await client.get("/api/v1/group")
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }


async def test_get_group_without_auth(client: AsyncClient):
    response = await client.get("/api/v1/group/1")
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }


async def test_put_group_without_auth(client: AsyncClient):
    response = await client.put("/api/v1/group/1")
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }
