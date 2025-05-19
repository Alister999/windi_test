import pytest
from httpx import AsyncClient


pytestmark = pytest.mark.asyncio


async def test_post_message_without_auth(client: AsyncClient):
    response = await client.post("/api/v1/message")
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }


async def test_delete_message_without_auth(client: AsyncClient):
    response = await client.delete("/api/v1/message/1")
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }


async def test_get_messages_without_auth(client: AsyncClient):
    response = await client.get("/api/v1/message")
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }


async def test_get_message_without_auth(client: AsyncClient):
    response = await client.get("/api/v1/message/1")
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }


async def test_put_message_without_auth(client: AsyncClient):
    response = await client.put("/api/v1/message/1")
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }


async def test_get_message_history_without_auth(client: AsyncClient):
    response = await client.get("/api/v1/history/1")
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }