import uvicorn


def main() -> None:
    uvicorn.run("tasks_api.tasks:app", reload=True)
