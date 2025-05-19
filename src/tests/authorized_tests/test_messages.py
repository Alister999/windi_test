import uuid
import pytest
from httpx import AsyncClient


pytestmark = pytest.mark.asyncio


async def test_post_message(client: AsyncClient):
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
    post_chat_response = await client.post(f"/api/v1/chat", json=chat_data, headers=headers)
    chat_id = post_chat_response.json()["id"]

    message_data = {
        "chat_id": chat_id,
        "text": "Text",
        "client_message_id": str(uuid.uuid4()),
        "sender_id": user_id
    }
    post_message_response = await client.post(f"/api/v1/message", json=message_data, headers=headers)

    assert post_message_response.status_code == 200

    expected_keys = {"id", "chat_id", "group_id", "sender_id", "text", "client_message_id", "is_read", "timestamp"}
    assert set(post_message_response.json().keys()) == expected_keys
    assert post_message_response.json()["chat_id"] == chat_id
    assert post_message_response.json()["group_id"] == None
    assert post_message_response.json()["sender_id"] == user_id
    assert post_message_response.json()["text"] == "Text"
    assert post_message_response.json()["is_read"] == "unread"


async def test_delete_message(client: AsyncClient):
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
    post_chat_response = await client.post(f"/api/v1/chat", json=chat_data, headers=headers)
    chat_id = post_chat_response.json()["id"]

    message_data = {
        "chat_id": chat_id,
        "text": "Text",
        "client_message_id": str(uuid.uuid4()),
        "sender_id": user_id
    }
    post_message_response = await client.post(f"/api/v1/message", json=message_data, headers=headers)
    message_id = post_message_response.json()["id"]

    get_response = await client.get(f"/api/v1/message", headers=headers)
    assert get_response.status_code == 200
    assert len(get_response.json()) == 1

    del_response = await client.delete(f"/api/v1/message/{message_id}", headers=headers)
    assert del_response.status_code == 200
    assert del_response.json() == {'message': f"Message with id '{message_id}' was deleted successful"}

    get_response = await client.get(f"/api/v1/message", headers=headers)
    assert get_response.status_code == 200
    assert len(get_response.json()) == 0


async def test_get_messages(client: AsyncClient):
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
    post_chat_response = await client.post(f"/api/v1/chat", json=chat_data, headers=headers)
    chat_id = post_chat_response.json()["id"]

    message_data = {
        "chat_id": chat_id,
        "text": "Text",
        "client_message_id": str(uuid.uuid4()),
        "sender_id": user_id
    }
    await client.post(f"/api/v1/message", json=message_data, headers=headers)

    response = await client.get("/api/v1/message", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_message(client: AsyncClient):
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
    post_chat_response = await client.post(f"/api/v1/chat", json=chat_data, headers=headers)
    chat_id = post_chat_response.json()["id"]

    message_data = {
        "chat_id": chat_id,
        "text": "Text",
        "client_message_id": str(uuid.uuid4()),
        "sender_id": user_id
    }
    message_post_response = await client.post(f"/api/v1/message", json=message_data, headers=headers)

    message_id = message_post_response.json()["id"]
    response = await client.get(f"/api/v1/message/{message_id}", headers=headers)
    assert response.status_code == 200

    expected_keys = {"id", "chat_id", "group_id", "sender_id", "text", "client_message_id", "is_read", "timestamp"}
    assert set(response.json().keys()) == expected_keys
    assert response.json()["chat_id"] == chat_id
    assert response.json()["group_id"] == None
    assert response.json()["sender_id"] == user_id
    assert response.json()["text"] == "Text"
    assert response.json()["is_read"] == "unread"


async def test_put_message(client: AsyncClient):
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
    post_chat_response = await client.post(f"/api/v1/chat", json=chat_data, headers=headers)
    chat_id = post_chat_response.json()["id"]

    message_data = {
        "chat_id": chat_id,
        "text": "Text",
        "client_message_id": str(uuid.uuid4()),
        "sender_id": user_id
    }

    message_data_2 = {
        "chat_id": chat_id,
        "text": "Text2",
        "client_message_id": str(uuid.uuid4()),
        "sender_id": user_id
    }
    message_post_response = await client.post(f"/api/v1/message", json=message_data, headers=headers)
    message_id = message_post_response.json()["id"]

    response = await client.put(f"/api/v1/message/{message_id}", json=message_data_2, headers=headers)

    assert response.status_code == 200

    expected_keys = {"id", "chat_id", "group_id", "sender_id", "text", "client_message_id", "is_read", "timestamp"}
    assert set(response.json().keys()) == expected_keys
    assert response.json()["chat_id"] == chat_id
    assert response.json()["group_id"] == None
    assert response.json()["sender_id"] == user_id
    assert response.json()["text"] == "Text2"
    assert response.json()["is_read"] == "unread"


async def test_get_history_messages(client: AsyncClient):
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
    post_chat_response = await client.post(f"/api/v1/chat", json=chat_data, headers=headers)
    chat_id = post_chat_response.json()["id"]

    message_data = {
        "chat_id": chat_id,
        "text": "Text",
        "client_message_id": str(uuid.uuid4()),
        "sender_id": user_id
    }
    await client.post("/api/v1/message", json=message_data, headers=headers)

    response = await client.get(f"/api/v1/history/{chat_id}", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1