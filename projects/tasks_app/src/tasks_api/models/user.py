"""SQLAlchemy models for tasks API."""

from sqlalchemy import Boolean, Column, Integer, String
from tasks_api.database import Base

# This type/class is used to create the database tables.


class User(Base):
    """User model representing the users table."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    phone_number = Column(String(255))
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    role = Column(String(255), default="user")  # Default role is 'user'
