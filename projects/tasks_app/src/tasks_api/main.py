"""CLI entry point for tasks API."""

import uvicorn

from .database import init_db


def main() -> None:
    init_db()
    uvicorn.run("tasks_api.app:app", reload=True)


if __name__ == "__main__":
    main()
