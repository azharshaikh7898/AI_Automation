from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.task import Task
from app.models.trigger import Trigger
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate


def list_tasks(db: Session, offset: int = 0, limit: int = 100) -> list[Task]:
    """
    Return a paginated list of tasks ordered by newest first.
    """
    statement = select(Task).order_by(Task.created_at.desc()).offset(offset).limit(limit)
    return list(db.scalars(statement).all())


def get_task(db: Session, task_id: int) -> Task | None:
    """
    Fetch a task by primary key.
    """
    return db.get(Task, task_id)


def _get_customer_or_404(db: Session, customer_id: int) -> Customer:
    customer = db.get(Customer, customer_id)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer


def _get_user_or_404(db: Session, user_id: int) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def _get_trigger_or_404(db: Session, trigger_id: int) -> Trigger:
    trigger = db.get(Trigger, trigger_id)
    if trigger is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trigger not found")
    return trigger


def create_task(db: Session, payload: TaskCreate) -> Task:
    """
    Create a new task record.
    """
    _get_customer_or_404(db, payload.customer_id)

    if payload.assigned_user_id is not None:
        _get_user_or_404(db, payload.assigned_user_id)

    if payload.trigger_id is not None:
        _get_trigger_or_404(db, payload.trigger_id)

    completed_at = datetime.now(timezone.utc) if payload.status == "completed" else None
    task = Task(
        customer_id=payload.customer_id,
        assigned_user_id=payload.assigned_user_id,
        trigger_id=payload.trigger_id,
        title=payload.title.strip(),
        description=payload.description,
        status=payload.status,
        priority=payload.priority,
        due_date=payload.due_date,
        completed_at=completed_at,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task: Task, payload: TaskUpdate) -> Task:
    """
    Update an existing task record.
    """
    update_data = payload.model_dump(exclude_unset=True)

    if "customer_id" in update_data and update_data["customer_id"] is not None:
        _get_customer_or_404(db, update_data["customer_id"])

    if "assigned_user_id" in update_data and update_data["assigned_user_id"] is not None:
        _get_user_or_404(db, update_data["assigned_user_id"])

    if "trigger_id" in update_data and update_data["trigger_id"] is not None:
        _get_trigger_or_404(db, update_data["trigger_id"])

    for field_name, value in update_data.items():
        if field_name == "title" and value is not None:
            value = value.strip()
        setattr(task, field_name, value)

    if "status" in update_data:
        if task.status == "completed":
            task.completed_at = task.completed_at or datetime.now(timezone.utc)
        else:
            task.completed_at = None

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    """
    Delete a task record.
    """
    db.delete(task)
    db.commit()