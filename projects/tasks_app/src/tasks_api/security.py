"""Security utilities for tasks API."""

import os
from datetime import UTC, datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from tasks_api.models.user import User

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(username: str, password: str, db: Session) -> User | None:
    """Authenticate a user."""
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        return None
    if not bcrypt_context.verify(password, user.hashed_password):
        return None
    return user


def create_access_token(
    username: str, user_id: int, role: str, expires_delta: timedelta
) -> str:
    """Create a JWT access token."""
    encode = {"sub": username, "id": user_id, "role": role}
    expires = datetime.now(UTC) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(
        encode, os.environ["SECRET_KEY"], algorithm=os.environ["ALGORITHM"]
    )
