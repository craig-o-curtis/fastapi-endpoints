SECRET_KEY="your_secret_key_here"
RAND=<get this by doing ...>
ALGORITHM="HS256"
# PostgreSQL, comment out to use SQLite db
DATABASE_URL=postgresql+psycopg://postgres:<pw>@localhost:5432/TasksApplicationDatabase
