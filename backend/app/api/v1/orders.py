from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.db.session import get_db
from app.models.user import User
from app.schemas.order import OrderCreate, OrderRead, OrderUpdate
from app.services.order_service import create_order, delete_order, get_order, list_orders, update_order


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("", response_model=list[OrderRead])
def read_orders(
    offset: int = 0,
    limit: int = 100,
    _: object = Depends(require_roles("Admin", "Manager", "Sales Executive")),
    db: Session = Depends(get_db),
) -> list[OrderRead]:
    """
    List orders with basic pagination.
    """
    return list_orders(db, offset=offset, limit=limit)


@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order_route(
    payload: OrderCreate,
    current_user: User = Depends(require_roles("Admin", "Manager", "Sales Executive")),
    db: Session = Depends(get_db),
) -> OrderRead:
    """
    Create a new order. If created_by_id is missing, the current user is used.
    """
    order_payload = payload.model_copy()
    if order_payload.created_by_id is None:
        order_payload.created_by_id = current_user.id
    return create_order(db, order_payload)


@router.get("/{order_id}", response_model=OrderRead)
def read_order(
    order_id: int,
    _: object = Depends(require_roles("Admin", "Manager", "Sales Executive")),
    db: Session = Depends(get_db),
) -> OrderRead:
    """
    Read a single order by id.
    """
    order = get_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.patch("/{order_id}", response_model=OrderRead)
def update_order_route(
    order_id: int,
    payload: OrderUpdate,
    _: object = Depends(require_roles("Admin", "Manager", "Sales Executive")),
    db: Session = Depends(get_db),
) -> OrderRead:
    """
    Update an existing order.
    """
    order = get_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return update_order(db, order, payload)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order_route(
    order_id: int,
    _: object = Depends(require_roles("Admin", "Manager")),
    db: Session = Depends(get_db),
) -> None:
    """
    Delete an order record.
    """
    order = get_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    delete_order(db, order)
