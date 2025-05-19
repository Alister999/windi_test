import logging

import pytest
from httpx import AsyncClient

logger = logging.getLogger("AuthTests")


# @pytest.mark.asyncio
# async def test_post_registration(client: AsyncClient):
#     data = {
#       "name": "Nikola",
#       "email": "user@example.com",
#       "password": "123"
#     }
#     response = await client.post("/api/v1/register", json=data)
#     logger.info(f'responce = {response.json()}')
#
#     assert response.status_code == 200
#
#     expected_keys = {"id", "name", "email", "password_hash"}
#     assert set(response.json().keys()) == expected_keys
#     assert response.json()["name"] == "Nikola"
#     assert response.json()["email"] == "user@example.com"
#
#
# @pytest.mark.asyncio
# async def test_post_login(client: AsyncClient):
#     data = {
#       "name": "Nikola",
#       "email": "user@example.com",
#       "password": "123"
#     }
#     await client.post("/api/v1/register", json=data)
#
#     login_data = {
#       "name": "Nikola",
#       "password": "123"
#     }
#
#     response = await client.post("/api/v1/login", json=login_data)
#
#     assert response.status_code == 200
#
#     expected_keys = {"access_token", "refresh_token", "token_type"}
#     assert set(response.json().keys()) == expected_keys
#     assert response.json()["token_type"] == "bearer"
#
#
# @pytest.mark.asyncio
# async def test_get_users(client: AsyncClient):
#     data = {
#         "name": "Nikola",
#         "email": "user@example.com",
#         "password": "123"
#     }
#
#     login_data = {
#         "name": "Nikola",
#         "password": "123"
#     }
#
#     await client.post("/api/v1/register", json=data)
#     response = await client.post("/api/v1/login", json=login_data)
#     my_token = response.json()["access_token"]
#
#     headers = {"Authorization": f"Bearer {my_token}"}
#     response = await client.get("/api/v1/user", headers=headers)
#
#     assert response.status_code == 200
#     assert len(response.json()) == 1
#
#     expected_keys = {"id", "name", "email", "password_hash"}
#     assert set(response.json()[0].keys()) == expected_keys
#     assert response.json()[0]["name"] == "Nikola"
#     assert response.json()[0]["email"] == "user@example.com"
#
#
# @pytest.mark.asyncio
# async def test_get_user(client: AsyncClient):
#     data = {
#         "name": "Nikola",
#         "email": "user@example.com",
#         "password": "123"
#     }
#
#     login_data = {
#         "name": "Nikola",
#         "password": "123"
#     }
#
#     reg_response = await client.post("/api/v1/register", json=data)
#     user_id = reg_response.json()["id"]
#
#     response = await client.post("/api/v1/login", json=login_data)
#     my_token = response.json()["access_token"]
#
#     headers = {"Authorization": f"Bearer {my_token}"}
#     response = await client.get(f"/api/v1/user/{user_id}", headers=headers)
#
#     assert response.status_code == 200
#     expected_keys = {"id", "name", "email", "password_hash"}
#     assert set(response.json().keys()) == expected_keys
#     assert response.json()["name"] == "Nikola"
#     assert response.json()["email"] == "user@example.com"
#
#
# @pytest.mark.asyncio
# async def test_delete_user(client: AsyncClient):
#     data = {
#         "name": "Nikola",
#         "email": "user@example.com",
#         "password": "123"
#     }
#
#     data2 = {
#         "name": "Bells",
#         "email": "user1@example.com",
#         "password": "123"
#     }
#
#     login_data = {
#         "name": "Nikola",
#         "password": "123"
#     }
#
#     await client.post("/api/v1/register", json=data)
#     second_reg = await client.post("/api/v1/register", json=data2)
#     delete_user_id = second_reg.json()["id"]
#     response = await client.post("/api/v1/login", json=login_data)
#     my_token = response.json()["access_token"]
#
#     headers = {"Authorization": f"Bearer {my_token}"}
#     get_response = await client.get("/api/v1/user", headers=headers)
#
#     assert get_response.status_code == 200
#     assert len(get_response.json()) == 2
#
#     delete_response = await client.delete(f"/api/v1/delete_user/{delete_user_id}", headers=headers)
#     assert delete_response.status_code == 200
#     assert delete_response.json() == {'message': f'User with id {delete_user_id} was deleted successful'}
#
#     get_response_2 = await client.get("/api/v1/user", headers=headers)
#
#     assert get_response_2.status_code == 200
#     assert len(get_response_2.json()) == 1
#
#
# @pytest.mark.asyncio
# async def test_refresh_user(client: AsyncClient):
#     data = {
#         "name": "Nikola",
#         "email": "user@example.com",
#         "password": "123"
#     }
#
#     login_data = {
#         "name": "Nikola",
#         "password": "123"
#     }
#
#     await client.post("/api/v1/register", json=data)
#     response = await client.post("/api/v1/login", json=login_data)
#     my_access_token = response.json()["access_token"]
#     my_refresh_token = response.json()["refresh_token"]
#
#     refresh_data = {
#       "refresh_token": my_refresh_token
#     }
#
#     refresh_response = await client.post("/api/v1/refresh", json=refresh_data)
#
#     expected_keys = {"access_token", "token_type"}
#     assert set(refresh_response.json().keys()) == expected_keys
#     assert response.json()["token_type"] == "bearer"
#
#     my_new_access_token = refresh_response.json()["access_token"]
#
#     headers = {"Authorization": f"Bearer {my_access_token}"}
#     get_response = await client.get("/api/v1/user", headers=headers)
#
#     assert get_response.status_code == 200
#
#     headers = {"Authorization": f"Bearer {my_new_access_token}"}
#     get_response = await client.get("/api/v1/user", headers=headers)
#
#     assert get_response.status_code == 200
#
#
# @pytest.mark.asyncio
# async def test_put_user(client: AsyncClient):
#     data = {
#         "name": "Nikola",
#         "email": "user@example.com",
#         "password": "123"
#     }
#
#     data_2 = {
#         "name": "Nikolay",
#         "email": "usersss@example.com",
#         "password": "1234"
#     }
#
#     login_data = {
#         "name": "Nikola",
#         "password": "123"
#     }
#
#     reg_response = await client.post("/api/v1/register", json=data)
#     user_id = reg_response.json()["id"]
#     response = await client.post("/api/v1/login", json=login_data)
#     my_access_token = response.json()["access_token"]
#
#     headers = {"Authorization": f"Bearer {my_access_token}"}
#     put_response = await client.put(f"/api/v1/user/{user_id}", json=data_2, headers=headers)
#
#     print(f"put response = {put_response.json()}")
#
#     assert put_response.status_code == 200
#
#     expected_keys = {"id", "name", "email", "password_hash"}
#     assert set(put_response.json().keys()) == expected_keys
#     assert put_response.json()["name"] == "Nikolay"
#     assert put_response.json()["email"] == "usersss@example.com"


