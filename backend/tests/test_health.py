"""
Tests for health check endpoints.
"""
from fastapi import status


def test_health_check(client):
    """Test basic health check endpoint."""
    response = client.get("/api/v1/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "healthy"
    assert "message" in data
    assert "timestamp" in data


def test_detailed_health_check(client):
    """Test detailed health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp" in data
    assert "components" in data
    assert data["components"]["api"] == "operational"
