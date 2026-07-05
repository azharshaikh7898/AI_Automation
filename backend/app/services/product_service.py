from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def list_products(db: Session, offset: int = 0, limit: int = 100) -> list[Product]:
    """
    Return a paginated list of products ordered by newest first.
    """
    statement = select(Product).order_by(Product.created_at.desc()).offset(offset).limit(limit)
    return list(db.scalars(statement).all())


def get_product(db: Session, product_id: int) -> Product | None:
    """
    Fetch a product by primary key.
    """
    return db.get(Product, product_id)


def _get_product_by_sku(db: Session, sku: str) -> Product | None:
    statement = select(Product).where(Product.sku == sku)
    return db.scalar(statement)


def create_product(db: Session, payload: ProductCreate) -> Product:
    """
    Create a new product record.
    """
    if _get_product_by_sku(db, payload.sku) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A product with this SKU already exists",
        )

    product = Product(
        name=payload.name.strip(),
        sku=payload.sku,
        description=payload.description,
        unit_price=payload.unit_price,
        stock_quantity=payload.stock_quantity,
        is_active=payload.is_active,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product: Product, payload: ProductUpdate) -> Product:
    """
    Update an existing product record.
    """
    update_data = payload.model_dump(exclude_unset=True)

    if "sku" in update_data and update_data["sku"] is not None:
        existing_product = _get_product_by_sku(db, update_data["sku"])
        if existing_product is not None and existing_product.id != product.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A product with this SKU already exists",
            )

    for field_name, value in update_data.items():
        if field_name == "name" and value is not None:
            value = value.strip()
        setattr(product, field_name, value)

    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product: Product) -> None:
    """
    Delete a product record.
    """
    db.delete(product)
    db.commit()
