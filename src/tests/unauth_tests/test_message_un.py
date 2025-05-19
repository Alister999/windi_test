import pytest
from fastapi.testclient import TestClient
from src.main import app

pytestmark = pytest.mark.asyncio

@pytest.fixture
def client():
    return TestClient(app=app)

# async def test_post_message_without_auth(client: TestClient):
#     response = client.post("/api/v1/message")
#     assert response.status_code == 401, f"Expected status 401, received {response.status_code}"
#     assert response.json() == {
#         "detail": "Not authenticated"
#     }
#
#     app.dependency_overrides.clear()
#
# async def test_delete_message_without_auth(client: TestClient):
#     response = client.delete("/api/v1/message/1")
#     assert response.status_code == 401, f"Expected status 401, received {response.status_code}"
#     assert response.json() == {
#         "detail": "Not authenticated"
#     }
#
#     app.dependency_overrides.clear()
#
#
# async def test_get_messages_without_auth(client: TestClient):
#     response = client.get("/api/v1/message")
#     assert response.status_code == 401, f"Expected status 401, received {response.status_code}"
#     assert response.json() == {
#         "detail": "Not authenticated"
#     }
#
#     app.dependency_overrides.clear()
#
# async def test_get_message_without_auth(client: TestClient):
#     response = client.get("/api/v1/message/1")
#     assert response.status_code == 401, f"Expected status 401, received {response.status_code}"
#     assert response.json() == {
#         "detail": "Not authenticated"
#     }
#
#     app.dependency_overrides.clear()
#
# async def test_put_message_without_auth(client: TestClient):
#     response = client.put("/api/v1/message/1")
#     assert response.status_code == 401, f"Expected status 401, received {response.status_code}"
#     assert response.json() == {
#         "detail": "Not authenticated"
#     }
#
#     app.dependency_overrides.clear()
#
# async def test_get_message_history_without_auth(client: TestClient):
#     response = client.get("/api/v1/history/1")
#     assert response.status_code == 401, f"Expected status 401, received {response.status_code}"
#     assert response.json() == {
#         "detail": "Not authenticated"
#     }
#
#     app.dependency_overrides.clear()