"""SQLAlchemy models for tasks API."""

from sqlalchemy import Boolean, Column, Integer, String
from tasks_api.database import Base

# This type/class is used to create the database tables.


class User(Base):
    """User model representing the users table."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")  # Default role is 'user'
