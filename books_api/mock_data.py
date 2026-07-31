from .models import Book

BOOKS: dict[int, Book] = {
    1: Book(
        id=1,
        title="Title One",
        author="Author One",
        category="science",
        description="A book about biology",
        rating=5,
    ),
    2: Book(
        id=2,
        title="Title Two",
        author="Author Two",
        category="science",
        description="A book about astronomy",
        rating=4,
    ),
    3: Book(
        id=3,
        title="Title Three",
        author="Author Three",
        category="history",
        description="A book about world history",
        rating=3,
    ),
    4: Book(
        id=4,
        title="Title Four",
        author="Author Four",
        category="math",
        description="A book about geometry",
        rating=2,
    ),
    5: Book(
        id=5,
        title="Title Five",
        author="Author Five",
        category="math",
        description="A book about calculus",
        rating=1,
    ),
    6: Book(
        id=6,
        title="Title Six",
        author="Author Two",
        category="math",
        description="A book about trigonometry",
        rating=1,
    ),
}
