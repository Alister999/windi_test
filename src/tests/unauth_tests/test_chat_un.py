import pytest
from httpx import AsyncClient


pytestmark = pytest.mark.asyncio


async def test_post_chat_without_auth(client: AsyncClient):
    response = await client.post("/api/v1/chat")
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }


async def test_delete_chat_without_auth(client: AsyncClient):
    response = await client.delete("/api/v1/chat/1")
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }


async def test_get_chats_without_auth(client: AsyncClient):
    response = await client.get("/api/v1/chat")
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }


async def test_get_chat_without_auth(client: AsyncClient):
    response = await client.get("/api/v1/chat/1")
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }


async def test_put_chat_without_auth(client: AsyncClient):
    response = await client.put("/api/v1/chat/1")
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }
