import pytest
from httpx import AsyncClient


pytestmark = pytest.mark.asyncio


async def test_post_chat(client: AsyncClient):
    data = {
        "name": "Nikola",
        "email": "user@example.com",
        "password": "123"
    }

    login_data = {
        "name": "Nikola",
        "password": "123"
    }

    reg_response = await client.post("/api/v1/register", json=data)
    user_id = reg_response.json()["id"]
    response = await client.post("/api/v1/login", json=login_data)
    my_access_token = response.json()["access_token"]

    chat_data = {
        "name_chat": "First chat",
        "type": "personal",
        "creator_id": user_id,
        "user_ids": [
            user_id
        ]
    }

    headers = {"Authorization": f"Bearer {my_access_token}"}
    post_response = await client.post(f"/api/v1/chat", json=chat_data, headers=headers)

    assert post_response.status_code == 200

    expected_keys = {"id", "name_chat", "type", "creator_id", "users"}
    assert set(post_response.json().keys()) == expected_keys
    assert post_response.json()["name_chat"] == "First chat"
    assert post_response.json()["type"] == "personal"
    assert post_response.json()["creator_id"] == user_id


async def test_delete_chat(client: AsyncClient):
    data = {
        "name": "Nikola",
        "email": "user@example.com",
        "password": "123"
    }

    login_data = {
        "name": "Nikola",
        "password": "123"
    }

    reg_response = await client.post("/api/v1/register", json=data)
    user_id = reg_response.json()["id"]
    response = await client.post("/api/v1/login", json=login_data)
    my_access_token = response.json()["access_token"]

    chat_data = {
        "name_chat": "First chat",
        "type": "personal",
        "creator_id": user_id,
        "user_ids": [
            user_id
        ]
    }

    headers = {"Authorization": f"Bearer {my_access_token}"}
    chat_post_response = await client.post(f"/api/v1/chat", json=chat_data, headers=headers)
    chat_id = chat_post_response.json()["id"]

    get_response = await client.get(f"/api/v1/chat", headers=headers)
    assert get_response.status_code == 200
    assert len(get_response.json()) == 1


    del_response = await client.delete(f"/api/v1/chat/{chat_id}", headers=headers)
    assert del_response.status_code == 200
    assert del_response.json() == {'message': f"Chat with id '{chat_id}' was deleted successful"}

    get_response = await client.get(f"/api/v1/chat", headers=headers)
    assert get_response.status_code == 200
    assert len(get_response.json()) == 0


async def test_get_chats(client: AsyncClient):
    data = {
        "name": "Nikola",
        "email": "user@example.com",
        "password": "123"
    }

    login_data = {
        "name": "Nikola",
        "password": "123"
    }

    reg_response = await client.post("/api/v1/register", json=data)
    user_id = reg_response.json()["id"]
    response = await client.post("/api/v1/login", json=login_data)
    my_access_token = response.json()["access_token"]

    chat_data = {
        "name_chat": "First chat",
        "type": "personal",
        "creator_id": user_id,
        "user_ids": [
            user_id
        ]
    }

    headers = {"Authorization": f"Bearer {my_access_token}"}
    await client.post(f"/api/v1/chat", json=chat_data, headers=headers)

    response = await client.get("/api/v1/chat", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_chat(client: AsyncClient):
    data = {
        "name": "Nikola",
        "email": "user@example.com",
        "password": "123"
    }

    login_data = {
        "name": "Nikola",
        "password": "123"
    }

    reg_response = await client.post("/api/v1/register", json=data)
    user_id = reg_response.json()["id"]
    response = await client.post("/api/v1/login", json=login_data)
    my_access_token = response.json()["access_token"]

    chat_data = {
        "name_chat": "First chat",
        "type": "personal",
        "creator_id": user_id,
        "user_ids": [
            user_id
        ]
    }

    headers = {"Authorization": f"Bearer {my_access_token}"}
    chat_post_response = await client.post(f"/api/v1/chat", json=chat_data, headers=headers)
    chat_id = chat_post_response.json()["id"]

    response = await client.get(f"/api/v1/chat/{chat_id}", headers=headers)

    assert response.status_code == 200

    expected_keys = {"id", "name_chat", "type", "creator_id", "users"}
    assert set(response.json().keys()) == expected_keys
    assert response.json()["name_chat"] == "First chat"
    assert response.json()["type"] == "personal"
    assert response.json()["creator_id"] == user_id


async def test_put_chat(client: AsyncClient):
    data = {
        "name": "Nikola",
        "email": "user@example.com",
        "password": "123"
    }

    login_data = {
        "name": "Nikola",
        "password": "123"
    }

    reg_response = await client.post("/api/v1/register", json=data)
    user_id = reg_response.json()["id"]
    response = await client.post("/api/v1/login", json=login_data)
    my_access_token = response.json()["access_token"]

    chat_data = {
        "name_chat": "First chat",
        "type": "personal",
        "creator_id": user_id,
        "user_ids": [
            user_id
        ]
    }

    chat_data_2 = {
        "name_chat": "First",
        "type": "group",
        "creator_id": user_id,
        "user_ids": []
    }

    headers = {"Authorization": f"Bearer {my_access_token}"}
    chat_post_response = await client.post(f"/api/v1/chat", json=chat_data, headers=headers)
    chat_id = chat_post_response.json()["id"]

    response = await client.put(f"/api/v1/chat/{chat_id}", json=chat_data_2, headers=headers)

    assert response.status_code == 200

    expected_keys = {"id", "name_chat", "type", "creator_id", "users"}
    assert set(response.json().keys()) == expected_keys
    assert response.json()["name_chat"] == "First"
    assert response.json()["type"] == "group"
    assert response.json()["creator_id"] == user_id
