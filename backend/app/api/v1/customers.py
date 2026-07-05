from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.db.session import get_db
from app.schemas.customer import CustomerCreate, CustomerRead, CustomerUpdate
from app.services.customer_service import create_customer, delete_customer, get_customer, list_customers, update_customer


router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("", response_model=list[CustomerRead])
def read_customers(
    offset: int = 0,
    limit: int = 100,
    _: object = Depends(require_roles("Admin", "Manager", "Sales Executive")),
    db: Session = Depends(get_db),
) -> list[CustomerRead]:
    """
    List customers with basic pagination.
    """
    return list_customers(db, offset=offset, limit=limit)


@router.post("", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
def create_customer_route(
    payload: CustomerCreate,
    _: object = Depends(require_roles("Admin", "Manager", "Sales Executive")),
    db: Session = Depends(get_db),
) -> CustomerRead:
    """
    Create a new customer.
    """
    return create_customer(db, payload)


@router.get("/{customer_id}", response_model=CustomerRead)
def read_customer(
    customer_id: int,
    _: object = Depends(require_roles("Admin", "Manager", "Sales Executive")),
    db: Session = Depends(get_db),
) -> CustomerRead:
    """
    Read a single customer by id.
    """
    customer = get_customer(db, customer_id)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer


@router.patch("/{customer_id}", response_model=CustomerRead)
def update_customer_route(
    customer_id: int,
    payload: CustomerUpdate,
    _: object = Depends(require_roles("Admin", "Manager", "Sales Executive")),
    db: Session = Depends(get_db),
) -> CustomerRead:
    """
    Update an existing customer.
    """
    customer = get_customer(db, customer_id)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return update_customer(db, customer, payload)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer_route(
    customer_id: int,
    _: object = Depends(require_roles("Admin", "Manager")),
    db: Session = Depends(get_db),
) -> None:
    """
    Delete a customer record.
    """
    customer = get_customer(db, customer_id)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    delete_customer(db, customer)
