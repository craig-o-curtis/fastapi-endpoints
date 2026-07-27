from __future__ import annotations

from fastapi.testclient import TestClient

from books_api.books import app

client = TestClient(app)


def test_root() -> None:
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Books API"
    assert data["status"] == "running"


def test_read_all_books() -> None:
    response = client.get("/books")
    assert response.status_code == 200
    books = response.json()
    assert len(books) == 6


def test_read_book_by_id_found() -> None:
    response = client.get("/books/1")
    assert response.status_code == 200
    book = response.json()
    assert book["title"] == "Title One"


def test_read_book_by_id_not_found() -> None:
    response = client.get("/books/999")
    assert response.status_code == 404


def test_filter_by_category_case_insensitive() -> None:
    response = client.get("/books/categories/science")
    assert response.status_code == 200
    books = response.json()
    assert len(books) == 2
    assert all(b["category"] == "science" for b in books)

    response = client.get("/books/categories/SCIENCE")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_filter_by_author_case_insensitive() -> None:
    response = client.get("/books/authors/Author%20One")
    assert response.status_code == 200
    books = response.json()
    assert len(books) == 1
    assert books[0]["author"] == "Author One"

    response = client.get("/books/authors/author%20one")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_filter_by_title_case_insensitive() -> None:
    response = client.get("/books/titles/Title%20One")
    assert response.status_code == 200
    books = response.json()
    assert len(books) == 1
    assert books[0]["title"] == "Title One"


def test_filter_no_results() -> None:
    response = client.get("/books/categories/fantasy")
    assert response.status_code == 404
