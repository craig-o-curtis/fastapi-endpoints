"""Route handlers for tasks API."""

from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query
from starlette import status

from .dependencies import DbDep
from .models import Tasks
from .schemas import TaskPost, TaskPut, TaskRead

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskRead])
def get_all_tasks(
    db: DbDep,
    skip: Annotated[int, Query(ge=0, description="Number of tasks to skip")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="Max tasks to return")] = 100,
) -> list[TaskRead]:
    """Get all tasks with pagination."""
    return [
        TaskRead.model_validate(t)
        for t in db.query(Tasks).offset(skip).limit(limit).all()
    ]


@router.get("/{task_id}", response_model=TaskRead)
def get_task_by_id(
    db: DbDep,
    task_id: Annotated[int, Path(gt=0, description="Task ID")],
) -> TaskRead:
    """Get a single task by ID."""
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskRead.model_validate(task)


@router.post("/", response_model=TaskRead, status_code=201)
def create_task(
    db: DbDep,
    task: TaskPost,
) -> TaskRead:
    """Create a new task."""
    task_model = Tasks(**task.model_dump())

    # db.add lets session know that we want to add this object to the database.
    db.add(task_model)
    # db.commit() is used to commit the changes to the database.
    db.commit()
    # db.refresh() is used to refresh the object from the database.
    db.refresh(task_model)
    return TaskRead.model_validate(task_model)


@router.put("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_task(
    db: DbDep,
    task_id: Annotated[int, Path(gt=0, description="Task ID")],
    task: TaskPut,
) -> None:  # <-- Change from TaskPut to None
    """Update an existing task."""
    task_model = db.query(Tasks).filter(Tasks.id == task_id).first()
    if task_model is None:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(task_model, key, value)
    db.commit()
    db.refresh(task_model)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    db: DbDep,
    task_id: Annotated[int, Path(gt=0, description="Task ID")],
) -> None:
    """Delete a task."""
    task_model = db.query(Tasks).filter(Tasks.id == task_id).first()
    if task_model is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task_model)
    db.commit()
