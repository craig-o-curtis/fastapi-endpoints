from typing import Annotated

from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field

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
    summary="List all books in the collection",
    description="Retrieve all books in the collection.",
    response_description="A list of books",
)
def read_all_books() -> list[Book]:
    """Retrieve all books."""
    return list(BOOKS.values())


@app.get(
    "/books/{book_id}",
    summary="Get a book by ID",
    description="Retrieve a single book by its unique identifier.",
    response_description="The requested book",
    responses={
        404: {"description": "Book not found with the specified ID."},
    },
)
def read_book(
    book_id: BookIdPath,
) -> Book:
    """
    Fetch a single book by its ID.

    The ID must be a positive integer.
    """
    book = BOOKS.get(book_id)
    if book is None:
        raise HTTPException(
            status_code=404,
            detail=f"Book with ID {book_id} not found.",
        )
    return book


@app.get(
    "/books/categories/{category}",
    summary="Get books by category",
    description="Retrieve all books that belong to the specified category.",
    response_description="A list of books in the category",
    responses={
        404: {"description": "No books found for the specified category."},
    },
)
def read_books_by_category(
    category: CategoryPath,
) -> list[Book]:
    """
    Fetch all books in a given category.

    The category name is case-sensitive.
    """
    filtered = [book for book in BOOKS.values() if book.category == category]
    if not filtered:
        raise HTTPException(
            status_code=404,
            detail=f"No books found in category: {category}",
        )
    return filtered


# read_books_by_author
@app.get(
    "/books/authors/{author}",
    summary="Get books by author",
    description="Retrieve all books that belong to the specified author.",
    response_description="A list of books in the author",
    responses={
        404: {"description": "No books found for the specified author."},
    },
)
def read_books_by_author(
    author: AuthorPath,
) -> list[Book]:
    """
    Fetch all books in a given author.

    The author name is case-sensitive.
    """
    filtered = [book for book in BOOKS.values() if book.author == author]
    if not filtered:
        raise HTTPException(
            status_code=404,
            detail=f"No books found in author: {author}",
        )
    return filtered


# get book by title
@app.get(
    "/books/titles/{title}",
    summary="Get books by title",
    description="Retrieve all books that belong to the specified title.",
    response_description="A list of books in the title",
    responses={
        404: {"description": "No books found for the specified title."},
    },
)
def read_books_by_title(
    title: TitlePath,
) -> list[Book]:
    """
    Fetch all books in a given title.

    The title name is case-sensitive.
    """
    filtered = [book for book in BOOKS.values() if book.title == title]
    if not filtered:
        raise HTTPException(
            status_code=404,
            detail=f"No books found in title: {title}",
        )
    return filtered
