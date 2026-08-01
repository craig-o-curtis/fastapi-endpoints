from typing import Annotated

from fastapi import Path

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
