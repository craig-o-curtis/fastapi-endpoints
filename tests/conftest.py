import pytest
from fastapi.testclient import TestClient

from books_api.books import app


@pytest.fixture
def api_client() -> TestClient:
    return TestClient(app)