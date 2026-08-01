from typing import Annotated

from fastapi import Query

CategoryQuery = Annotated[
    str | None,
    Query(max_length=50, description="The category to filter books by."),
]

AuthorQuery = Annotated[
    str | None,
    Query(max_length=100, description="The author to filter books by."),
]

TitleQuery = Annotated[
    str | None,
    Query(max_length=100, description="The title to filter books by."),
]

DescriptionQuery = Annotated[
    str | None,
    Query(max_length=100, description="The description to filter books by."),
]

RatingQuery = Annotated[
    int | None,
    Query(ge=1, le=5, description="The rating to filter books by."),
]
