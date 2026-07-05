from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.db.session import get_db
from app.schemas.trigger import TriggerCreate, TriggerRead, TriggerUpdate
from app.services.trigger_service import create_trigger, delete_trigger, get_trigger, list_triggers, update_trigger


router = APIRouter(prefix="/triggers", tags=["Triggers"])


@router.get("", response_model=list[TriggerRead])
def read_triggers(
    offset: int = 0,
    limit: int = 100,
    _: object = Depends(require_roles("Admin", "Manager")),
    db: Session = Depends(get_db),
) -> list[TriggerRead]:
    """
    List triggers with basic pagination.
    """
    return list_triggers(db, offset=offset, limit=limit)


@router.post("", response_model=TriggerRead, status_code=status.HTTP_201_CREATED)
def create_trigger_route(
    payload: TriggerCreate,
    _: object = Depends(require_roles("Admin", "Manager")),
    db: Session = Depends(get_db),
) -> TriggerRead:
    """
    Create a new trigger.
    """
    return create_trigger(db, payload)


@router.get("/{trigger_id}", response_model=TriggerRead)
def read_trigger(
    trigger_id: int,
    _: object = Depends(require_roles("Admin", "Manager")),
    db: Session = Depends(get_db),
) -> TriggerRead:
    """
    Read a single trigger by id.
    """
    trigger = get_trigger(db, trigger_id)
    if trigger is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trigger not found")
    return trigger


@router.patch("/{trigger_id}", response_model=TriggerRead)
def update_trigger_route(
    trigger_id: int,
    payload: TriggerUpdate,
    _: object = Depends(require_roles("Admin", "Manager")),
    db: Session = Depends(get_db),
) -> TriggerRead:
    """
    Update an existing trigger.
    """
    trigger = get_trigger(db, trigger_id)
    if trigger is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trigger not found")
    return update_trigger(db, trigger, payload)


@router.delete("/{trigger_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trigger_route(
    trigger_id: int,
    _: object = Depends(require_roles("Admin", "Manager")),
    db: Session = Depends(get_db),
) -> None:
    """
    Delete a trigger record.
    """
    trigger = get_trigger(db, trigger_id)
    if trigger is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trigger not found")
    delete_trigger(db, trigger)