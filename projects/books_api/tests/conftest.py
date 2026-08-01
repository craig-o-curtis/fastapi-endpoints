import pytest
from books_api.books import app
from fastapi.testclient import TestClient


@pytest.fixture
def api_client() -> TestClient:
    return TestClient(app)
