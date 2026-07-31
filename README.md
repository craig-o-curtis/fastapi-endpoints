# Books API

A simple FastAPI project to manage a collection of books.

## Setup

```bash
# Install dependencies (runtime + dev) using uv
uv sync
```

> Dependencies are declared in `pyproject.toml`. There is no `requirements.txt`.

## Run

```bash
# Development (with auto-reload)
uv run uvicorn books_api.books:app --reload

# Or via FastAPI CLI
uv run fastapi dev books_api/books.py
```

Server starts at `http://127.0.0.1:8000`.

## Test

```bash
# -v enables verbose output
uv run pytest -v tests/
```

## Lint and type check

```bash
# Lint with ruff
uv run ruff check books_api/ tests/

# Format check
uv run ruff format --check books_api/ tests/

# Type check with ty
uv run ty check books_api/ tests/
```

## Command reference

| Task           | Without `uv`                                                                                      | With `uv`                                      |
| -------------- | ------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| Setup          | `python3 -m venv .fastapienv` \
`source .fastapienv/bin/activate` \
`pip install -e ".[dev]"` | `uv sync` |
| Run dev server | `uvicorn books_api.books:app --reload`                                                            | `uv run uvicorn books_api.books:app --reload`  |
| Run tests      | `pytest -v tests/`                                                                                | `uv run pytest -v tests/`                      |
| Lint           | `ruff check books_api/ tests/`                                                                    | `uv run ruff check books_api/ tests/`          |
| Format check   | `ruff format --check books_api/ tests/`                                                           | `uv run ruff format --check books_api/ tests/` |
| Type check     | `ty check books_api/ tests/`                                                                      | `uv run ty check books_api/ tests/`            |

## Reference

- `pyproject.toml` — single source of truth for dependencies, tool config, and project metadata
- `books_api/` — application code
- `tests/` — pytest test suite

## Learning

- [docs/packages.md](docs/packages.md) — explanations of every package in this project (FastAPI, Pydantic, Uvicorn, Ruff, ty, etc.)
