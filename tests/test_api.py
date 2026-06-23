from fastapi.testclient import TestClient


def test_health_check(client: TestClient) -> None:
    """Verifies that the health check endpoint returns 200 and valid JSON data."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert data["environment"] == "testing"
    assert "uptime_seconds" in data
    assert "version" in data


def test_root_redirect(client: TestClient) -> None:
    """Verifies that the root path '/' redirects to the Swagger UI page '/docs'."""
    # follow_redirects=False to verify redirection status
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/docs"


def test_correlation_id_middleware(client: TestClient) -> None:
    """Verifies that the correlation ID header is generated and returned in headers."""
    response = client.get("/api/v1/health")
    assert "X-Correlation-ID" in response.headers
    assert len(response.headers["X-Correlation-ID"]) > 0


def test_correlation_id_propagation(client: TestClient) -> None:
    """Verifies that a client-sent correlation ID is preserved and returned."""
    test_id = "test-correlation-123"
    response = client.get("/api/v1/health", headers={"X-Correlation-ID": test_id})
    assert response.headers["X-Correlation-ID"] == test_id


def test_items_crud_flow(client: TestClient) -> None:
    """Tests the full CRUD cycle for the items API endpoints."""
    # 1. List items (should contain the 2 default seed items)
    response = client.get("/api/v1/items")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 2
    assert items[0]["name"] == "Screwdriver"
    assert items[1]["name"] == "Hammer"

    # 2. Create new item
    new_item_payload = {
        "name": "Chisel",
        "description": "Wood carving chisel",
        "price": 8.50,
        "tax": 0.80,
    }
    create_response = client.post("/api/v1/items", json=new_item_payload)
    assert create_response.status_code == 201
    created_data = create_response.json()
    assert "id" in created_data
    created_id = created_data["id"]
    assert created_data["name"] == "Chisel"

    # 3. Retrieve created item
    get_response = client.get(f"/api/v1/items/{created_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Chisel"

    # 4. Attempt to create duplicate item (should return 400 Bad Request)
    dup_response = client.post("/api/v1/items", json=new_item_payload)
    assert dup_response.status_code == 400
    assert dup_response.json()["code"] == "DUPLICATE_ITEM"

    # 5. Update the item
    update_payload = {"price": 9.99, "description": "Updated wood carving chisel"}
    put_response = client.put(f"/api/v1/items/{created_id}", json=update_payload)
    assert put_response.status_code == 200
    updated_data = put_response.json()
    assert updated_data["price"] == 9.99
    assert updated_data["description"] == "Updated wood carving chisel"

    # 6. Delete the item
    del_response = client.delete(f"/api/v1/items/{created_id}")
    assert del_response.status_code == 204

    # 7. Verify deletion (get should return 404)
    get_deleted_response = client.get(f"/api/v1/items/{created_id}")
    assert get_deleted_response.status_code == 404
    assert get_deleted_response.json()["code"] == "NOT_FOUND"


def test_validation_errors(client: TestClient) -> None:
    """Verifies that invalid input yields structured 422 validation error lists."""
    bad_payload = {
        "name": "",  # Too short (min_length=1)
        "price": -10.0,  # Must be positive (gt=0.0)
    }
    response = client.post("/api/v1/items", json=bad_payload)
    assert response.status_code == 422

    data = response.json()
    assert data["code"] == "VALIDATION_ERROR"
    assert "details" in data
    assert len(data["details"]) == 2


def test_repository_dependency_override(client: TestClient) -> None:
    """Verifies that the items repository can be swapped dynamically
    using dependency overrides (DIP).
    """
    from typing import Any

    from star_wars_api_wrapper.api.v1.endpoints.items import get_items_repository
    from star_wars_api_wrapper.main import app
    from star_wars_api_wrapper.repositories.base import BaseItemsRepository

    class DummyRepository(BaseItemsRepository):
        async def list(self, skip: int = 0, limit: int = 10) -> list[dict[str, Any]]:
            return [
                {
                    "id": 99,
                    "name": "Dummy Item",
                    "description": "Mocked",
                    "price": 1.0,
                    "tax": 0.1,
                }
            ]

        async def get(self, item_id: int) -> dict[str, Any] | None:
            return None

        async def create(self, item_in: Any) -> dict[str, Any]:
            return {}

        async def update(self, item_id: int, item_in: Any) -> dict[str, Any] | None:
            return None

        async def delete(self, item_id: int) -> bool:
            return False

    app.dependency_overrides[get_items_repository] = lambda: DummyRepository()

    try:
        response = client.get("/api/v1/items")
        assert response.status_code == 200
        items = response.json()
        assert len(items) == 1
        assert items[0]["id"] == 99
        assert items[0]["name"] == "Dummy Item"
    finally:
        app.dependency_overrides.clear()
