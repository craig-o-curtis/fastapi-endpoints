# Books API

A simple FastAPI project to manage a collection of books.

## Setup

```bash
# Create virtual environment
python3 -m venv .fastapienv

# Activate
source .fastapienv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install all dependencies (runtime + dev) from pyproject.toml
pip install -e ".[dev]"
```

> Dependencies are declared in `pyproject.toml`. There is no `requirements.txt`.

## Run

```bash
# Development (with auto-reload)
uvicorn books_api.books:app --reload

# Or via FastAPI CLI
fastapi dev books_api/books.py
```

Server starts at `http://127.0.0.1:8000`.

## Docs

Available at [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs)

## Test

```bash
# 
# source .fastapienv/bin/activate
pytest -v
# or
pytest -v tests/
```

> If you get `ModuleNotFoundError: No module named 'books_api'`, run the dependency setup first:
> ```bash
> pip install -e ".[dev]"
> ```

## Lint and type check

```bash
# Lint with ruff
ruff check books_api/ tests/

# Type check with ty
ty check books_api/ tests/
```

## Reference

- `pyproject.toml` — single source of truth for dependencies, tool config, and project metadata
- `books_api/` — application code
- `tests/` — pytest test suite
