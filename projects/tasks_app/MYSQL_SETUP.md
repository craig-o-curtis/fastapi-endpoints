# MySQL Setup

Two ways to run MySQL for the Tasks API: **Docker Compose** (isolated, disposable) or **local MySQL Mac app** (persistent, manual control). Pick one.

## Toggle: Docker Compose vs Local MySQL

| Feature          | Docker Compose            | Local MySQL Mac app                      |
| ---------------- | ------------------------- | ---------------------------------------- |
| MySQL location   | Docker container          | Running locally on `localhost:3306`      |
| Admin GUI        | Adminer (port `8080`)     | Use your installed Mac app               |
| Data persistence | Docker volume `mysqldata` | Local MySQL data directory               |
| Best for         | Fresh starts, CI, sharing | Existing local DB, manual schema control |

### Option A: Docker Compose (recommended for fresh starts)

> **Sanity check:** If you already have MySQL running locally on port `3306`, stop it first before bringing up the stack.

1. Start the stack from `projects/tasks_app/`:

    ```bash
    docker compose -f src/tasks_api/docker-compose.mysql.yml up -d
    ```

2. Verify both services are healthy:

    ```bash
    docker compose -f src/tasks_api/docker-compose.mysql.yml ps
    ```

    You should see `mysql` and `adminer` with state `Up`.

3. Confirm MySQL is reachable:

    ```bash
    docker compose -f src/tasks_api/docker-compose.mysql.yml exec mysql mysqladmin ping -h localhost -u root -p12345678
    ```

4. Open Adminer in your browser:
   - URL: `http://localhost:8080`

5. Log in to Adminer:
   - System: `MySQL`
   - Server: `mysql`
   - Username: `root`
    - Password: `12345678`
    - Database: `tasks_application_database`
6. Seed the schema and admin user (see below).

### Option B: Local MySQL Mac App

1. Start your local MySQL server (e.g. via Homebrew or the Mac app).

2. Create the database if needed:

    ```bash
    mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS tasks_application_database;"
    ```

3. Connect using Adminer (if running via Docker) or a local client like Sequel Ace:
    - Server: `localhost`
    - Port: `3306`
    - Username: `root`
    - Password: `<your local root password>`
 4. Seed the schema and admin user (see below).

## Seeding the Database

**Tables are created by Alembic migrations.** After starting MySQL, run:

```bash
uv run alembic upgrade head
```

This applies the initial migration and creates `users` and `tasks` tables.

The steps below are for **local MySQL clients** or if you want to reset the schema manually. Only Step 2 (admin user) is truly required to get a working login.

### 1. Run migrations (or create tables manually)

If you're using Adminer or a local MySQL client and want to create/reset the schema manually:

```sql
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS tasks;

CREATE TABLE users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    role VARCHAR(255) DEFAULT 'user'
);

CREATE TABLE tasks(
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    description VARCHAR(255),
    priority INTEGER,
    completed BOOLEAN DEFAULT FALSE,
    owner_id INTEGER,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);
```

Alternatively, use Alembic (recommended for ongoing development):

```bash
uv run alembic upgrade head
```

### 2. Create admin user (required for login)

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

### Verify app connects to MySQL

Start the API:

```bash
uv run tasks-api
```

In another terminal, confirm the app is using MySQL (not SQLite or Postgres). If you see connection errors, check `.env`:

```bash
# projects/tasks_app/.env
DATABASE_URL=mysql+pymysql://root:12345678@localhost:3306/tasks_application_database
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

To toggle between MySQL, Postgres, and SQLite, edit `.env`:

```bash
# MySQL (requires running DB)
DATABASE_URL=mysql+pymysql://root:12345678@localhost:3306/tasks_application_database

# PostgreSQL
DATABASE_URL=postgresql+psycopg://postgres:12345678@localhost:5432/TasksApplicationDatabase

# SQLite (default local file)
# DATABASE_URL=
```

Restart the app after changing `.env`. After switching, apply migrations to the new database:

```bash
uv run alembic upgrade head
```

## Resetting Data

### Docker Compose

```bash
docker compose -f src/tasks_api/docker-compose.mysql.yml down -v   # WARNING: deletes all data in mysqldata volume
docker compose -f src/tasks_api/docker-compose.mysql.yml up -d
docker compose -f src/tasks_api/docker-compose.mysql.yml ps
```

### Local MySQL

```bash
mysql -u root -p -e "DROP DATABASE tasks_application_database; CREATE DATABASE tasks_application_database;"
uv run alembic upgrade head
```
