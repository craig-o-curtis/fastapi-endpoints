from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status
from tasks_api.dependencies.db_dep import DbDep
from tasks_api.models.user import User
from tasks_api.schemas.users import (
    CreateUserRequest,
    ReadUserRequest,
    UpdateUserRequest,
)
from tasks_api.security import bcrypt_context

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[ReadUserRequest])
def read_users(db: DbDep) -> list[ReadUserRequest]:
    """Get all users."""
    users = db.query(User).all()
    return [ReadUserRequest.model_validate(user) for user in users]


@router.get("/{user_id}", response_model=ReadUserRequest)
def read_user(
    db: DbDep,
    user_id: int = Path(gt=0, description="User ID"),
) -> ReadUserRequest:
    """Get a single user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return ReadUserRequest.model_validate(user)


@router.post("", response_model=ReadUserRequest, status_code=status.HTTP_201_CREATED)
def create_user(db: DbDep, user: CreateUserRequest) -> ReadUserRequest:
    """Create a new user."""
    user_model = User(
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
        hashed_password=bcrypt_context.hash(user.password),
        is_active=True,
    )

    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return ReadUserRequest.model_validate(user_model)


@router.put("/{user_id}", response_model=ReadUserRequest)
def update_user(
    db: DbDep,
    user_id: Annotated[int, Path(gt=0, description="User ID")],
    user: UpdateUserRequest,
) -> ReadUserRequest:
    """Update an existing user."""
    user_model = db.query(User).filter(User.id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(user_model, key, value)

    db.commit()
    db.refresh(user_model)
    return ReadUserRequest.model_validate(user_model)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    db: DbDep,
    user_id: Annotated[int, Path(gt=0, description="User ID")],
) -> None:
    """Delete a user."""
    user_model = db.query(User).filter(User.id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user_model)
    db.commit()
