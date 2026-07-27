from fastapi import FastAPI

app = FastAPI()


BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "history"},
    {"title": "Title Four", "author": "Author Four", "category": "math"},
    {"title": "Title Five", "author": "Author Five", "category": "math"},
    {"title": "Title Six", "author": "Author Two", "category": "math"},
]


@app.get("/")
async def root():
    return {
        "name": "Books API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/books")
async def read_all_books():
    """
    Fetches a list of all books in the database.
    Returns:
        A list of dictionaries, where each dictionary represents a book with its title, author, and category.
    """
    print("Fetching list of books...")
    return BOOKS
