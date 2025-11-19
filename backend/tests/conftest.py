"""
Pytest configuration and shared fixtures.
"""
import pytest
from fastapi.testclient import TestClient
from src.api.main import app


@pytest.fixture
def client():
    """
    Fixture providing a test client for the FastAPI application.
    
    Returns:
        TestClient: FastAPI test client
    """
    return TestClient(app)
