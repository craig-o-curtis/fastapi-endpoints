"""SQLAlchemy models for tasks API."""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from tasks_api.database import Base


class Task(Base):
    """Task model representing the tasks table."""

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    priority = Column(Integer, index=True)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
