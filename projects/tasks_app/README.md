# Tasks App

## Architecture

Standard FastAPI project layout, split by responsibility so each file has one job:

| File              | Responsibility                                                                                                | Why it's separate                                                                                                      |
| ----------------- | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `app.py`          | App factory — creates the `FastAPI()` instance, sets metadata, wires up routers                               | Single source of truth for the `app` object; both `main.py` and any ASGI server (uvicorn/gunicorn) import it from here |
| `main.py`         | CLI entry point (`tasks-api` script, see `pyproject.toml`); calls `init_db()` then starts uvicorn with reload | Keeps `app.py` importable (e.g. in tests) without triggering DB init or starting a server                              |
| `config.py`       | Environment-driven settings (currently just `DATABASE_URL`, defaulting to local SQLite)                       | Centralizes config reads so nothing else touches `os.getenv` directly                                                  |
| `database.py`     | SQLAlchemy engine, session factory (`SessionLocal`), declarative `Base`, and `init_db()`                      | Table creation is explicit at startup, not an import-time side effect                                                  |
| `models.py`       | SQLAlchemy ORM models — the DB table shape                                                                    | One class per table, isolated from the API contract                                                                    |
| `schemas.py`      | Pydantic models — the API's request/response shape (`TaskRead`, `TaskPost`)                                   | Lets the DB schema and public API contract evolve independently                                                        |
| `dependencies.py` | FastAPI `Depends` providers, e.g. `get_db` / `DbDep` for per-request DB sessions                              | Shared across routers via import instead of being redefined per file                                                   |
| `routers.py`      | `APIRouter` with endpoint handlers, grouped by resource (`/tasks`)                                            | Keeps route logic out of `app.py`; new resources get their own router module as the app grows                          |

This mirrors the common "layered" FastAPI convention: **routing** (routers) → **contracts** (schemas) → **persistence** (models/database) → **wiring** (dependencies/config), with `app.py` tying it together and `main.py` as the runnable entry point. It intentionally stops there — no service layer, no repository pattern, no DI container — because the app is small enough that those would add indirection without paying for itself yet. Reach for that structure later only if routers start doing non-trivial business logic beyond basic CRUD.

## Run db

```bash
# Dive in to /data dir
cd projects/tasks_app/data


# Run
sqlite3 tasks.db

# Stop
.quit
```

## SQL basics

### Create

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    priority INTEGER,
    completed BOOLEAN DEFAULT FALSE
);
```

### Insert

```sql
INSERT INTO tasks (title, description, priority, completed) VALUES ('Task 1', 'Description 1', 1, FALSE);

INSERT INTO tasks (title, description, priority, completed) VALUES ('Task 2', 'Description 2', 5, FALSE);
```

### Select

```sql
SELECT * FROM tasks;

SELECT id, title, description, priority, completed FROM tasks;

SELECT title, description, priority, completed FROM tasks WHERE id = 1;

SELECT * FROM tasks WHERE completed = FALSE;
```

### Update

```sql
UPDATE tasks
SET title = 'Task 1 Updated'
WHERE id = 1;

UPDATE tasks
SET completed = TRUE
WHERE id = 1;
```

### Delete

```sql
DELETE FROM tasks
WHERE id = 1;
```

### Drop

```sql
DROP TABLE tasks;
```

## Tips

Column mode

```sql
.mode column
select * from tasks;
```

Markdown mode

```sql
.mode markdown
select * from tasks;
```

Box mode

```sql
.mode box
select * from tasks;
```

Table mode

```sql
.mode table
select * from tasks;
```

Headers on

```sql
.headers on
select * from tasks;
```
