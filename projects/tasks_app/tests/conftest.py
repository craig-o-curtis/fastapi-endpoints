import tempfile
from collections.abc import Generator

import pytest
from fastapi import Depends
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tasks_api.app import app
from tasks_api.database import Base
from tasks_api.dependencies.db_dep import get_db
from tasks_api.dependencies.user_dep import get_current_user
from tasks_api.models.task import Task
from tasks_api.models.user import User
from tasks_api.security import bcrypt_context

_FAKE_HASH = bcrypt_context.hash("fakepass123")
_SECRET = "test-secret-key-for-testing-only"
_ALGO = "HS256"


def _make_token(username: str, user_id: int, role: str) -> str:
    """Create a test JWT access token."""
    from datetime import UTC, datetime, timedelta

    encode = {
        "sub": username,
        "id": user_id,
        "role": role,
        "exp": datetime.now(UTC) + timedelta(hours=1),
    }
    return jwt.encode(encode, _SECRET, algorithm=_ALGO)


@pytest.fixture
def fake_user() -> User:
    """Create a fake user for testing authenticated endpoints."""
    return User(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_password=_FAKE_HASH,
        is_active=True,
        role="user",
    )


@pytest.fixture
def fake_second_user() -> User:
    """Create a second fake user for owner isolation tests."""
    return User(
        id=3,
        username="seconduser",
        email="second@example.com",
        hashed_password=_FAKE_HASH,
        is_active=True,
        role="user",
    )


@pytest.fixture
def fake_admin_user() -> User:
    """Create a fake admin user for testing admin endpoints."""
    return User(
        id=2,
        username="adminuser",
        email="admin@example.com",
        hashed_password=_FAKE_HASH,
        is_active=True,
        role="admin",
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

    # Insert the user into the DB so authenticate_user can find them
    with TestSessionLocal() as db:
        db.add(fake_user)
        db.commit()
        db.refresh(fake_user)

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

    def override_get_current_user(db=Depends(get_db)) -> User:
        return db.query(User).filter(User.id == fake_user.id).first()

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    yield TestClient(app)
    app.dependency_overrides.clear()
    engine.dispose()


@pytest.fixture
def admin_client(fake_admin_user: User) -> Generator[TestClient]:
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as db_file:
        db_path = db_file.name
    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
    )
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    # Insert the admin user into the DB so admin endpoints can find it
    with TestSessionLocal() as db:
        db.add(fake_admin_user)
        db.commit()
        db.refresh(fake_admin_user)

    task = Task(
        title="Admin Test Task",
        description="A task for admin testing.",
        owner_id=fake_admin_user.id,
    )
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

    def override_get_current_user(db=Depends(get_db)) -> User:
        return db.query(User).filter(User.id == fake_admin_user.id).first()

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    yield TestClient(app)
    app.dependency_overrides.clear()
    engine.dispose()


@pytest.fixture
def no_auth_client() -> Generator[TestClient]:
    """Client with no authentication override — for testing auth/login endpoints."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as db_file:
        db_path = db_file.name
    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
    )
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    # Insert a user so login can find them
    user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_password=_FAKE_HASH,
        is_active=True,
        role="user",
    )
    with TestSessionLocal() as db:
        db.add(user)
        db.commit()
        db.refresh(user)

    # Also store a token in the app so auth tests can use it
    app.state.test_token = _make_token("testuser", 1, "user")

    def override_get_db():
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    # Do NOT override get_current_user — auth endpoint doesn't use it,
    # but other endpoints would fail without auth. This fixture is for
    # testing the /auth/token endpoint only.
    yield TestClient(app)
    app.dependency_overrides.clear()
    engine.dispose()


@pytest.fixture
def isolation_client(fake_user: User, fake_second_user: User) -> Generator[TestClient]:
    """Client authenticated as user 1, but DB has a task owned by user 2.
    Used to test owner isolation — user 1 should NOT see/update/delete user 2's task.
    """
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as db_file:
        db_path = db_file.name
    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
    )
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    # Insert user 2's task (owned by fake_second_user, not fake_user)
    task = Task(
        title="Other User's Task",
        description="Owned by second user.",
        owner_id=fake_second_user.id,
    )
    with TestSessionLocal() as db:
        db.add(fake_second_user)
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
