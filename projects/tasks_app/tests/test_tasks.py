from fastapi.testclient import TestClient
from tasks_api.tasks import app

client = TestClient(app)


def test_root_health_check() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"
