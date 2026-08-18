from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from tasks_api.config import DATABASE_URL


def _get_connect_args(database_url: str) -> dict[str, object]:
    if database_url.startswith("sqlite"):
        return {"check_same_thread": False}
    return {}


engine = create_engine(DATABASE_URL, connect_args=_get_connect_args(DATABASE_URL))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# This is the base class for all models
class Base(DeclarativeBase):
    pass


# This function
def init_db() -> None:
    Base.metadata.create_all(bind=engine)
