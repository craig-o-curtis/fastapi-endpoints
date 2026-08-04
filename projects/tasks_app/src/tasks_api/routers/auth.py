from datetime import timedelta
from typing import Annotated, cast

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from tasks_api.dependencies.db_dep import DbDep
from tasks_api.schemas.token import Token
from tasks_api.security import authenticate_user, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: DbDep,
):
    """Login for access token."""
    user = authenticate_user(form_data.username, form_data.password, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user.",
        )
    # Here the cast fn is used to tell mypy (static type checker) that user.id is an int
    # and user.role is a str, even though they are Optional[int]
    # and Optional[str] respectively.
    # This is safe because we know that if user is not None,
    # then user.id and user.role will not be None.
    user_id = cast(int, user.id)
    user_role = cast(str, user.role)
    token = create_access_token(
        form_data.username, user_id, user_role, timedelta(minutes=20)
    )
    return Token(access_token=token, token_type="bearer")
