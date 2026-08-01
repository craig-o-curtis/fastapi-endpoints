from typing import Annotated

from fastapi import Body

from .models import BookCreate, BookUpdate

BookCreateBody = Annotated[BookCreate, Body()]
BookUpdateBody = Annotated[BookUpdate, Body()]
