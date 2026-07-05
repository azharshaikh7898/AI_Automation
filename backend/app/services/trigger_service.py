from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.trigger import Trigger
from app.schemas.trigger import TriggerCreate, TriggerUpdate


def list_triggers(db: Session, offset: int = 0, limit: int = 100) -> list[Trigger]:
    """
    Return a paginated list of triggers ordered by newest first.
    """
    statement = select(Trigger).order_by(Trigger.created_at.desc()).offset(offset).limit(limit)
    return list(db.scalars(statement).all())


def get_trigger(db: Session, trigger_id: int) -> Trigger | None:
    """
    Fetch a trigger by primary key.
    """
    return db.get(Trigger, trigger_id)


def _get_trigger_by_name(db: Session, name: str) -> Trigger | None:
    statement = select(Trigger).where(Trigger.name == name)
    return db.scalar(statement)


def create_trigger(db: Session, payload: TriggerCreate) -> Trigger:
    """
    Create a new trigger record.
    """
    if _get_trigger_by_name(db, payload.name) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A trigger with this name already exists",
        )

    trigger = Trigger(
        name=payload.name.strip(),
        trigger_type=payload.trigger_type,
        description=payload.description,
        condition_expression=payload.condition_expression,
        delay_minutes=payload.delay_minutes,
        is_active=payload.is_active,
    )
    db.add(trigger)
    db.commit()
    db.refresh(trigger)
    return trigger


def update_trigger(db: Session, trigger: Trigger, payload: TriggerUpdate) -> Trigger:
    """
    Update an existing trigger record.
    """
    update_data = payload.model_dump(exclude_unset=True)

    if "name" in update_data and update_data["name"] is not None:
        existing_trigger = _get_trigger_by_name(db, update_data["name"])
        if existing_trigger is not None and existing_trigger.id != trigger.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A trigger with this name already exists",
            )

    for field_name, value in update_data.items():
        setattr(trigger, field_name, value)

    db.add(trigger)
    db.commit()
    db.refresh(trigger)
    return trigger


def delete_trigger(db: Session, trigger: Trigger) -> None:
    """
    Delete a trigger record.
    """
    db.delete(trigger)
    db.commit()