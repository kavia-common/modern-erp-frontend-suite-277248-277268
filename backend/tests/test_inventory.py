"""
Tests for inventory endpoints.
"""
from fastapi import status


def test_list_inventory_items(client):
    """Test listing inventory items."""
    response = client.get("/api/v1/inventory/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "skip" in data
    assert "limit" in data
    assert isinstance(data["items"], list)
    assert data["total"] > 0


def test_get_inventory_item(client):
    """Test getting a specific inventory item."""
    response = client.get("/api/v1/inventory/1")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == 1
    assert "name" in data
    assert "sku" in data
    assert "quantity" in data


def test_create_inventory_item(client):
    """Test creating an inventory item."""
    new_item = {
        "name": "Test Item",
        "sku": "TEST-001",
        "category": "Test",
        "quantity": 100,
        "unit_price": 50.00,
        "reorder_level": 10,
        "description": "Test item description"
    }
    response = client.post("/api/v1/inventory/", json=new_item)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == new_item["name"]
    assert data["sku"] == new_item["sku"]
    assert "id" in data


def test_update_inventory_item(client):
    """Test updating an inventory item."""
    update_data = {
        "quantity": 150,
        "unit_price": 55.00
    }
    response = client.put("/api/v1/inventory/1", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["quantity"] == update_data["quantity"]
    assert data["unit_price"] == update_data["unit_price"]


def test_get_nonexistent_inventory_item(client):
    """Test getting a non-existent inventory item."""
    response = client.get("/api/v1/inventory/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_inventory_pagination(client):
    """Test inventory pagination."""
    response = client.get("/api/v1/inventory/?skip=0&limit=2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) <= 2
    assert data["skip"] == 0
    assert data["limit"] == 2
