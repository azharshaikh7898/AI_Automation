from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.user import User
from app.schemas.order import OrderCreate, OrderItemCreate, OrderUpdate


def list_orders(db: Session, offset: int = 0, limit: int = 100) -> list[Order]:
    """
    Return a paginated list of orders ordered by newest first.
    """
    statement = select(Order).order_by(Order.created_at.desc()).offset(offset).limit(limit)
    return list(db.scalars(statement).all())


def get_order(db: Session, order_id: int) -> Order | None:
    """
    Fetch an order by primary key.
    """
    return db.get(Order, order_id)


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


def _get_product_or_404(db: Session, product_id: int) -> Product:
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


def _get_order_by_number(db: Session, order_number: str) -> Order | None:
    statement = select(Order).where(Order.order_number == order_number)
    return db.scalar(statement)


def _build_order_item(db: Session, order_id: int, item_payload: OrderItemCreate) -> OrderItem:
    product = _get_product_or_404(db, item_payload.product_id)
    unit_price = item_payload.unit_price if item_payload.unit_price is not None else Decimal(product.unit_price)
    line_total = Decimal(unit_price) * Decimal(item_payload.quantity)
    return OrderItem(
        order_id=order_id,
        product_id=product.id,
        quantity=item_payload.quantity,
        unit_price=unit_price,
        line_total=line_total,
    )


def create_order(db: Session, payload: OrderCreate) -> Order:
    """
    Create a new order and its line items.
    """
    if _get_order_by_number(db, payload.order_number) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An order with this order number already exists",
        )

    _get_customer_or_404(db, payload.customer_id)

    if payload.created_by_id is not None:
        _get_user_or_404(db, payload.created_by_id)

    order = Order(
        customer_id=payload.customer_id,
        created_by_id=payload.created_by_id,
        order_number=payload.order_number,
        status=payload.status,
        currency=payload.currency,
        notes=payload.notes,
        total_amount=Decimal("0.00"),
    )
    db.add(order)
    db.flush()

    total_amount = Decimal("0.00")
    order_items: list[OrderItem] = []
    for item_payload in payload.items:
        order_item = _build_order_item(db, order.id, item_payload)
        total_amount += Decimal(order_item.line_total)
        order_items.append(order_item)

    db.add_all(order_items)
    order.total_amount = total_amount
    db.commit()
    db.refresh(order)
    return order


def update_order(db: Session, order: Order, payload: OrderUpdate) -> Order:
    """
    Update an existing order record.
    """
    update_data = payload.model_dump(exclude_unset=True)

    if "customer_id" in update_data and update_data["customer_id"] is not None:
        _get_customer_or_404(db, update_data["customer_id"])

    if "created_by_id" in update_data and update_data["created_by_id"] is not None:
        _get_user_or_404(db, update_data["created_by_id"])

    for field_name, value in update_data.items():
        setattr(order, field_name, value)

    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def delete_order(db: Session, order: Order) -> None:
    """
    Delete an order and its line items.
    """
    db.delete(order)
    db.commit()
