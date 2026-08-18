# Postgres Setup

Two ways to run PostgreSQL for the Tasks API: **Docker Compose** (isolated, disposable) or **local Postgres + pgAdmin4** (persistent, manual control). Pick one.

## Toggle: Docker Compose vs Local pgAdmin4

| Feature           | Docker Compose                | Local pgAdmin4                           |
| ----------------- | ----------------------------- | ---------------------------------------- |
| Postgres location | Docker container              | Running locally on `localhost:5432`      |
| pgAdmin4          | Included as `pgadmin` service | Use your installed Mac app               |
| Data persistence  | Docker volume `pgdata`        | Local Postgres data directory            |
| Best for          | Fresh starts, CI, sharing     | Existing local DB, manual schema control |

### Option A: Docker Compose (recommended for fresh starts)

> **Sanity check:** If you already have Postgres running locally on port `5432`, stop it first:
>
> ```bash
> # If using Homebrew
> brew services stop postgresql
> # Or
> pg_ctl -D /usr/local/var/postgres stop
> ```

0. Open up Docker Desktop

1. Start the stack from `projects/tasks_app/src/tasks_api/`:

   ```bash
   docker compose up -d
   ```

2. Verify both services are healthy:

   ```bash
   docker compose ps
   ```

   You should see `db` and `pgadmin` with state `Up`.

3. Confirm Postgres is reachable:

   ```bash
   docker compose exec db pg_isready -U postgres -d TasksApplicationDatabase
   ```

4. Open pgAdmin4 in your browser:
   - URL: `http://localhost:5050`
   - Email: `admin@example.com`
   - Password: `admin123`
5. In pgAdmin4, add a server connection:
   - Click **"Add New Server"** in the _Browser_ panel (left sidebar)
   - **General** tab:
     - Name: `Tasks DB` (or anything you like)
   - **Connection** tab:
     - Host: `db` (the docker service name)
     - Port: `5432`
     - Maintenance database: `TasksApplicationDatabase`
     - Username: `postgres`
     - Password: `12345678`
   - Click **Save**
   - You should now see `Tasks DB` under _Servers_ in the Browser panel. Expand it → _Databases_ → `TasksApplicationDatabase` → _Schemas_ → _Tables_
6. Seed the schema and admin user (see below).

### Option B: Local Postgres + pgAdmin4 Mac App

1. Start your local Postgres:

   ```bash
   # Homebrew example
   brew services start postgresql
   ```

2. Create the database if needed:

   ```bash
   createdb TasksApplicationDatabase
   ```

3. Open your **pgAdmin4 Mac app** and connect to `localhost:5432`.
4. Seed the schema and admin user (see below).

## Seeding the Database

Regardless of which option you used, run the SQL below in pgAdmin4's Query Tool to create tables and the admin user.

### 1. Create tables

```sql
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS tasks;

CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    role VARCHAR(255) DEFAULT 'user'
);

CREATE TABLE tasks(
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    description VARCHAR(500),
    priority INTEGER,
    completed BOOLEAN DEFAULT FALSE,
    owner_id INTEGER REFERENCES users(id)
);
```

### 2. Create admin user

Pick a password, then generate its bcrypt hash using the project venv:

```bash
/Users/craigcurtis/workbench/python/fastapi-backend/.venv/bin/python -c "
from passlib.context import CryptContext
c = CryptContext(schemes=['bcrypt'], deprecated='auto')
print(c.hash('YOUR_PASSWORD_HERE'))
"
```

Replace `YOUR_PASSWORD_HERE` with your chosen password, then run:

```sql
INSERT INTO users (username, email, first_name, last_name, hashed_password, is_active, role)
VALUES (
  'admin',
  'admin@example.com',
  'Admin',
  'User',
  '<paste-hash-here>',
  true,
  'admin'
);
```

## Sanity Checks

### Verify app connects to Postgres

Start the API:

```bash
uv run tasks-api
```

In another terminal, confirm the app is using Postgres (not SQLite). If you see Postgres connection errors, check `.env`:

```bash
# projects/tasks_app/.env
DATABASE_URL=postgresql+psycopg://postgres:<password>@localhost:5432/TasksApplicationDatabase
```

To force SQLite (local fallback), comment out `DATABASE_URL` in `.env`. The app will then use `data/tasksapp.db`.

### Test login

```bash
curl -X POST http://127.0.0.1:8000/auth/token \
  -d "username=admin" \
  -d "password=YOUR_PASSWORD_HERE"
```

You should get a JSON response with `access_token`.

## Switching Backends

To toggle between Postgres and SQLite, edit `.env`:

```bash
# Postgres (requires running DB)
DATABASE_URL=postgresql+psycopg://postgres:12345678@localhost:5432/TasksApplicationDatabase

# SQLite (default local file)
# DATABASE_URL=
```

Restart the app after changing `.env`.

## Resetting Data

### Docker Compose

```bash
docker compose down -v   # WARNING: deletes all data in pgdata volume
docker compose up -d
docker compose ps         # check containers are running
```

### Local Postgres

```bash
dropdb TasksApplicationDatabase
createdb TasksApplicationDatabase
# Then re-run the seed SQL above
```
