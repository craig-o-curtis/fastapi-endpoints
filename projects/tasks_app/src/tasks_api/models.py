"""SQLAlchemy models for tasks API."""

from sqlalchemy import Boolean, Column, Integer, String

from .database import Base


class Tasks(Base):
    """Task model representing the tasks table."""

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    priority = Column(Integer, index=True)
    completed = Column(Boolean, default=False)
