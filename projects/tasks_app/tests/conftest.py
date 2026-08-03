import tempfile
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tasks_api.app import app
from tasks_api.database import Base
from tasks_api.dependencies.db_dep import get_db
from tasks_api.dependencies.user_dep import get_current_user
from tasks_api.models.task import Task
from tasks_api.models.user import User


@pytest.fixture
def fake_user() -> User:
    """Create a fake user for testing authenticated endpoints."""
    return User(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_password="fake",
        is_active=True,
        role="user",
    )


@pytest.fixture
def api_client(fake_user: User) -> Generator[TestClient]:
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as db_file:
        db_path = db_file.name
    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
    )
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    task = Task(title="Test Task", description="A test task.", owner_id=fake_user.id)
    with TestSessionLocal() as db:
        db.add(task)
        db.commit()
        db.refresh(task)

    def override_get_db():
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()

    def override_get_current_user() -> User:
        return fake_user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    yield TestClient(app)
    app.dependency_overrides.clear()
    engine.dispose()
