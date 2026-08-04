"""Route handlers for tasks API."""

from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query
from starlette import status
from tasks_api.dependencies.db_dep import DbDep
from tasks_api.dependencies.user_dep import UserDep
from tasks_api.models.task import Task
from tasks_api.schemas.tasks import (
    CreateTaskRequest,
    ReadTaskRequest,
    UpdateTaskRequest,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[ReadTaskRequest])
def get_all_tasks(
    user: UserDep,
    db: DbDep,
    skip: Annotated[int, Query(ge=0, description="Number of tasks to skip")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="Max tasks to return")] = 100,
) -> list[ReadTaskRequest]:
    """Get all tasks with pagination."""

    return [
        ReadTaskRequest.model_validate(t)
        for t in db.query(Task)
        .filter(Task.owner_id == user.id)
        .offset(skip)
        .limit(limit)
        .all()
    ]


@router.get("/{task_id}", response_model=ReadTaskRequest)
def get_task_by_id(
    user: UserDep,
    db: DbDep,
    task_id: Annotated[int, Path(gt=0, description="Task ID")],
) -> ReadTaskRequest:
    """Get a single task by ID."""
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )

    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .filter(Task.owner_id == user.id)
        .first()
    )
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return ReadTaskRequest.model_validate(task)


@router.post("/", response_model=ReadTaskRequest, status_code=201)
def create_task(user: UserDep, db: DbDep, task: CreateTaskRequest) -> ReadTaskRequest:
    """Create a new task."""
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )

    task_model = Task(**task.model_dump(), owner_id=user.id)

    # db.add lets session know that we want to add this object to the database.
    db.add(task_model)
    # db.commit() is used to commit the changes to the database.
    db.commit()
    # db.refresh() is used to refresh the object from the database.
    db.refresh(task_model)
    return ReadTaskRequest.model_validate(task_model)


@router.put("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_task(
    user: UserDep,
    db: DbDep,
    task_id: Annotated[int, Path(gt=0, description="Task ID")],
    task: UpdateTaskRequest,
) -> None:  # <-- Change from UpdateTaskRequest to None
    """Update an existing task."""
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )

    task_model = (
        db.query(Task)
        .filter(Task.id == task_id)
        .filter(Task.owner_id == user.id)
        .first()
    )
    if task_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    for key, value in task.model_dump(exclude_unset=True).items():
        # skip updating the owner_id field to prevent changing the task's owner
        if key == "owner_id":
            continue
        setattr(task_model, key, value)
    db.commit()
    db.refresh(task_model)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    user: UserDep,
    db: DbDep,
    task_id: Annotated[int, Path(gt=0, description="Task ID")],
) -> None:
    """Delete a task."""
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )

    task_model = (
        db.query(Task)
        .filter(Task.id == task_id)
        .filter(Task.owner_id == user.id)
        .first()
    )
    if task_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    db.delete(task_model)
    db.commit()
