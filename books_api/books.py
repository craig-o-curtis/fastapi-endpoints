from typing import Annotated

from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field

from .api_utils import is_casefold_match, is_positive_integer

app = FastAPI(
    title="Books API",
    description="A simple API to manage a collection of books.",
    version="1.0.0",
)


class Book(BaseModel):
    id: int = Field(ge=1, description="The unique identifier of the book.")
    title: str = Field(max_length=100, description="The title of the book.")
    author: str = Field(max_length=100, description="The author of the book.")
    category: str = Field(
        max_length=50,
        description="The category or genre of the book.",
    )


# Annotation adds metadata, validation, documentation, and examples your parameters
BookIdPath = Annotated[
    int,
    Path(ge=1, description="The ID of the book to retrieve."),
]

CategoryPath = Annotated[
    str,
    Path(max_length=50, description="The category to filter books by."),
]

AuthorPath = Annotated[
    str,
    Path(max_length=100, description="The author to filter books by."),
]

TitlePath = Annotated[
    str,
    Path(max_length=100, description="The title to filter books by."),
]


BOOKS: dict[int, Book] = {
    1: Book(id=1, title="Title One", author="Author One", category="science"),
    2: Book(id=2, title="Title Two", author="Author Two", category="science"),
    3: Book(id=3, title="Title Three", author="Author Three", category="history"),
    4: Book(id=4, title="Title Four", author="Author Four", category="math"),
    5: Book(id=5, title="Title Five", author="Author Five", category="math"),
    6: Book(id=6, title="Title Six", author="Author Two", category="math"),
}


@app.get(
    "/",
    summary="Health check",
    description=(
        "Returns basic information about the API including name, version, and status."
    ),
    response_description="API metadata",
)
def root() -> dict[str, str]:
    """Get API status and metadata."""
    return {
        "name": "Books API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get(
    "/books",
)
def read_all_books() -> list[Book]:
    """Retrieve all books."""
    return list(BOOKS.values())


@app.get("/books/{book_id}")
def read_book_by_id(
    book_id: BookIdPath,
) -> Book:
    """
    Fetch a single book by its ID.

    The ID must be a positive integer.
    """
    if not is_positive_integer(book_id):
        raise HTTPException(
            status_code=422,
            detail=f"Book ID must be a positive integer. Received: {book_id}",
        )
    book = BOOKS.get(book_id)
    if book is None:
        raise HTTPException(
            status_code=404,
            detail=f"Book with ID {book_id} not found.",
        )
    return book


@app.get("/books/categories/{category}")
def read_books_by_category(
    category: CategoryPath,
) -> list[Book]:
    """
    Fetch all books in a given category.

    The category name is case-sensitive.
    """
    filtered = [
        book for book in BOOKS.values() if is_casefold_match(book.category, category)
    ]
    if not filtered:
        raise HTTPException(
            status_code=404,
            detail=f"No books found in category: {category}",
        )
    return filtered


# read_books_by_author
@app.get("/books/authors/{author}")
def read_books_by_author(
    author: AuthorPath,
) -> list[Book]:
    """
    Fetch all books in a given author.

    The author name is case-sensitive.
    """
    filtered = [
        book for book in BOOKS.values() if is_casefold_match(book.author, author)
    ]
    if not filtered:
        raise HTTPException(
            status_code=404,
            detail=f"No books found in author: {author}",
        )
    return filtered


# get book by title
@app.get("/books/titles/{title}")
def read_books_by_title(
    title: TitlePath,
) -> list[Book]:
    """
    Fetch all books in a given title.

    The title name is case-sensitive.
    """
    filtered = [book for book in BOOKS.values() if is_casefold_match(book.title, title)]
    if not filtered:
        raise HTTPException(
            status_code=404,
            detail=f"No books found in title: {title}",
        )
    return filtered
