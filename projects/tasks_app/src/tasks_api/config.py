"""Configuration for tasks API."""

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

load_dotenv(PROJECT_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "test-secret-key-for-testing-only")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{DATA_DIR / 'tasksapp.db'}",
)
