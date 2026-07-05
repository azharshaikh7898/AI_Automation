from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.db.session import get_db
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.task_service import create_task, delete_task, get_task, list_tasks, update_task


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", response_model=list[TaskRead])
def read_tasks(
    offset: int = 0,
    limit: int = 100,
    _: object = Depends(require_roles("Admin", "Manager", "Sales Executive")),
    db: Session = Depends(get_db),
) -> list[TaskRead]:
    """
    List tasks with basic pagination.
    """
    return list_tasks(db, offset=offset, limit=limit)


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task_route(
    payload: TaskCreate,
    _: object = Depends(require_roles("Admin", "Manager", "Sales Executive")),
    db: Session = Depends(get_db),
) -> TaskRead:
    """
    Create a new task.
    """
    return create_task(db, payload)


@router.get("/{task_id}", response_model=TaskRead)
def read_task(
    task_id: int,
    _: object = Depends(require_roles("Admin", "Manager", "Sales Executive")),
    db: Session = Depends(get_db),
) -> TaskRead:
    """
    Read a single task by id.
    """
    task = get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=TaskRead)
def update_task_route(
    task_id: int,
    payload: TaskUpdate,
    _: object = Depends(require_roles("Admin", "Manager", "Sales Executive")),
    db: Session = Depends(get_db),
) -> TaskRead:
    """
    Update an existing task.
    """
    task = get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return update_task(db, task, payload)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_route(
    task_id: int,
    _: object = Depends(require_roles("Admin", "Manager")),
    db: Session = Depends(get_db),
) -> None:
    """
    Delete a task record.
    """
    task = get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    delete_task(db, task)