from fastapi.testclient import TestClient


class TestRoot:
    def test_health_check(self, api_client: TestClient) -> None:
        """Verify the root endpoint returns the API name and running status."""
        response = api_client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Tasks App"
        assert data["status"] == "running"


class TestReadTasks:
    def test_get_all_tasks(self, api_client: TestClient) -> None:
        """Verify that all tasks can be retrieved."""
        response = api_client.get("/tasks")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestReadTask:
    def test_get_task(self, api_client: TestClient) -> None:
        """Verify that a task can be retrieved."""
        response = api_client.get("/tasks/1")
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_get_task_not_found(self, api_client: TestClient) -> None:
        """Verify that a task can be retrieved."""
        response = api_client.get("/tasks/999")
        assert response.status_code == 404

        assert response.json()["detail"] == "Task not found"

    def test_get_task_invalid_id(self, api_client: TestClient) -> None:
        """Verify that a task can be retrieved."""
        response = api_client.get("/tasks/abc")
        assert response.status_code == 422

        assert (
            response.json()["detail"][0]["msg"]
            == "Input should be a valid integer, unable to parse string as an integer"
        )


class TestCreateTask:
    def test_create_task(self, api_client: TestClient) -> None:
        """Verify that a task can be created."""
        new_task = {"title": "New Task", "description": "A new task to do."}
        response = api_client.post("/tasks", json=new_task)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == new_task["title"]
        assert data["description"] == new_task["description"]

    def test_create_task_invalid_data(self, api_client: TestClient) -> None:
        """Verify that a task can be created."""
        desc_only = {"description": "A new task to do."}
        response = api_client.post("/tasks", json=desc_only)
        assert response.status_code == 422

        assert response.json()["detail"][0]["msg"] == "Field required"

        priority_only = {"priority": 3}
        response = api_client.post("/tasks", json=priority_only)
        assert response.status_code == 422

        completed_only = {"completed": False}
        response = api_client.post("/tasks", json=completed_only)
        assert response.status_code == 422

        all_optional = {
            "description": "A new task to do.",
            "priority": 3,
            "completed": False,
        }
        response = api_client.post("/tasks", json=all_optional)
        assert response.status_code == 422


class TestUpdateTask:
    def test_update_task(self, api_client: TestClient) -> None:
        """Verify that a task can be updated."""
        update_data = {"title": "Updated Task", "description": "An updated task."}
        response = api_client.put("/tasks/1", json=update_data)
        assert response.status_code == 204
        assert response.content == b""  # <-- 204 has no body

    def test_update_task_not_found(self, api_client: TestClient) -> None:
        """Verify that a task can be updated."""
        update_data = {"title": "Updated Task", "description": "An updated task."}
        response = api_client.put("/tasks/999", json=update_data)
        assert response.status_code == 404

        assert response.json()["detail"] == "Task not found"

    def test_update_task_invalid_id(self, api_client: TestClient) -> None:
        """Verify that a task can be updated."""
        update_data = {"title": "Updated Task", "description": "An updated task."}
        response = api_client.put("/tasks/abc", json=update_data)
        assert response.status_code == 422

        assert (
            response.json()["detail"][0]["msg"]
            == "Input should be a valid integer, unable to parse string as an integer"
        )


class TestDeleteTask:
    def test_delete_task(self, api_client: TestClient) -> None:
        """Verify that a task can be deleted."""
        response = api_client.delete("/tasks/1")
        assert response.status_code == 204
        assert response.content == b""  # <-- 204 has no body

    def test_delete_task_not_found(self, api_client: TestClient) -> None:
        """Verify that a task can be deleted."""
        response = api_client.delete("/tasks/999")
        assert response.status_code == 404

        assert response.json()["detail"] == "Task not found"

    def test_delete_task_invalid_id(self, api_client: TestClient) -> None:
        """Verify that a task can be deleted."""
        response = api_client.delete("/tasks/abc")
        assert response.status_code == 422

        assert (
            response.json()["detail"][0]["msg"]
            == "Input should be a valid integer, unable to parse string as an integer"
        )
