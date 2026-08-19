"""CLI entry point for tasks API."""

import uvicorn


def main() -> None:
    uvicorn.run("tasks_api.app:app", reload=True)


if __name__ == "__main__":
    main()
