from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate


def list_customers(db: Session, offset: int = 0, limit: int = 100) -> list[Customer]:
    """
    Return a paginated list of customers ordered by newest first.
    """
    statement = select(Customer).order_by(Customer.created_at.desc()).offset(offset).limit(limit)
    return list(db.scalars(statement).all())


def get_customer(db: Session, customer_id: int) -> Customer | None:
    """
    Fetch a customer by primary key.
    """
    return db.get(Customer, customer_id)


def create_customer(db: Session, payload: CustomerCreate) -> Customer:
    """
    Create a new customer record.
    """
    customer = Customer(
        first_name=payload.first_name.strip(),
        last_name=payload.last_name.strip(),
        email=str(payload.email).strip().lower() if payload.email else None,
        phone_number=payload.phone_number,
        company_name=payload.company_name,
        assigned_user_id=payload.assigned_user_id,
        status=payload.status,
        source=payload.source,
        notes=payload.notes,
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def update_customer(db: Session, customer: Customer, payload: CustomerUpdate) -> Customer:
    """
    Update an existing customer record.
    """
    update_data = payload.model_dump(exclude_unset=True)
    for field_name, value in update_data.items():
        if field_name == "email" and value is not None:
            value = str(value).strip().lower()
        setattr(customer, field_name, value)

    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def delete_customer(db: Session, customer: Customer) -> None:
    """
    Delete a customer record.
    """
    db.delete(customer)
    db.commit()
