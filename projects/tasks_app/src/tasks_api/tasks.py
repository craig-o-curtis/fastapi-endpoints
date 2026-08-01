from fastapi import FastAPI

app = FastAPI(
    title="Tasks API",
    description="A simple API to manage a collection of tasks.",
    version="1.0.0",
)


@app.get(
    "/",
    summary="Health check",
    description=(
        "Returns basic information about the API including name, version, and status."
    ),
    response_description="API metadata",
)
def root() -> dict[str, str]:
    """Get API status and metadata."""
    return {
        "name": "Tasks API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }
