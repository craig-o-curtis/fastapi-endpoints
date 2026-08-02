"""FastAPI app factory for tasks API."""

from fastapi import FastAPI

from .routers import router

app = FastAPI(
    title="Tasks API",
    description="A simple API to manage a collection of tasks.",
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
def health_check() -> dict[str, str]:
    """Basic liveness check."""
    return {
        "name": "Tasks App",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }
