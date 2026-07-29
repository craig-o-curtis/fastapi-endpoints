from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from books_api.books import app


@pytest.fixture
def api_client() -> TestClient:
    return TestClient(app)


class TestRoot:
    def test_health_check(self, api_client: TestClient) -> None:
        """Verify the root endpoint returns the API name and running status."""
        response = api_client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Books API"
        assert data["status"] == "running"


class TestReadBooks:
    def test_read_all_books(self, api_client: TestClient) -> None:
        """Verify GET /books returns all books with a 200 status."""
        response = api_client.get("/books")
        assert response.status_code == 200
        books = response.json()
        assert len(books) == 6

    def test_read_book_by_id_found(self, api_client: TestClient) -> None:
        """Verify GET /books/{id} returns the matching book when it exists."""
        response = api_client.get("/books/1")
        assert response.status_code == 200
        book = response.json()
        assert book["title"] == "Title One"

    def test_read_book_by_id_not_found(self, api_client: TestClient) -> None:
        """Verify GET /books/{id} returns 404 when the book does not exist."""
        response = api_client.get("/books/999")
        assert response.status_code == 404

    def test_filter_by_category_case_insensitive(self, api_client: TestClient) -> None:
        """Verify category filtering is case-insensitive."""
        response = api_client.get("/books/categories/science")
        assert response.status_code == 200
        books = response.json()
        assert len(books) == 2
        assert all(b["category"] == "science" for b in books)

        response = api_client.get("/books/categories/SCIENCE")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_filter_by_author_case_insensitive(self, api_client: TestClient) -> None:
        """Verify author filtering is case-insensitive."""
        response = api_client.get("/books/authors/Author%20One")
        assert response.status_code == 200
        books = response.json()
        assert len(books) == 1
        assert books[0]["author"] == "Author One"

        response = api_client.get("/books/authors/author%20one")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_filter_by_title_case_insensitive(self, api_client: TestClient) -> None:
        """Verify title filtering is case-insensitive."""
        response = api_client.get("/books/titles/Title%20One")
        assert response.status_code == 200
        books = response.json()
        assert len(books) == 1
        assert books[0]["title"] == "Title One"

    def test_filter_no_results(self, api_client: TestClient) -> None:
        """Verify filtering with no matching results returns 404."""
        response = api_client.get("/books/categories/fantasy")
        assert response.status_code == 404


class TestCreateBook:
    def test_happy_path(self, api_client: TestClient) -> None:
        """Verify creating a book returns the created book with all fields."""
        response = api_client.post(
            "/books",
            json={"title": "New Book", "author": "New Author", "category": "fiction"},
        )
        assert response.status_code == 200
        book = response.json()
        assert book["title"] == "New Book"
        assert book["author"] == "New Author"
        assert book["category"] == "fiction"
        assert book["id"] == 7

    def test_duplicate_book_returns_409(self, api_client: TestClient) -> None:
        """Verify creating a duplicate book returns 409."""
        response = api_client.post(
            "/books",
            json={"title": "Title One", "author": "Author One", "category": "science"},
        )
        assert response.status_code == 409


class TestUpdateBook:
    def test_happy_path(self, api_client: TestClient) -> None:
        """Verify updating a book returns the updated book with all fields."""
        response = api_client.put(
            "/books/1",
            json={
                "title": "Updated Title",
                "author": "Updated Author",
                "category": "fiction",
            },
        )
        assert response.status_code == 200
        book = response.json()
        assert book["title"] == "Updated Title"
        assert book["author"] == "Updated Author"
        assert book["category"] == "fiction"
        assert book["id"] == 1

    def test_update_nonexistent_book_returns_404(self, api_client: TestClient) -> None:
        """Verify updating a nonexistent book returns 404."""
        response = api_client.put(
            "/books/999",
            json={
                "title": "Updated Title",
                "author": "Updated Author",
                "category": "fiction",
            },
        )
        assert response.status_code == 404
