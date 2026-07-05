from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services.product_service import create_product, delete_product, get_product, list_products, update_product


router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=list[ProductRead])
def read_products(
    offset: int = 0,
    limit: int = 100,
    _: object = Depends(require_roles("Admin", "Manager", "Sales Executive")),
    db: Session = Depends(get_db),
) -> list[ProductRead]:
    """
    List products with basic pagination.
    """
    return list_products(db, offset=offset, limit=limit)


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product_route(
    payload: ProductCreate,
    _: object = Depends(require_roles("Admin", "Manager", "Sales Executive")),
    db: Session = Depends(get_db),
) -> ProductRead:
    """
    Create a new product.
    """
    return create_product(db, payload)


@router.get("/{product_id}", response_model=ProductRead)
def read_product(
    product_id: int,
    _: object = Depends(require_roles("Admin", "Manager", "Sales Executive")),
    db: Session = Depends(get_db),
) -> ProductRead:
    """
    Read a single product by id.
    """
    product = get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.patch("/{product_id}", response_model=ProductRead)
def update_product_route(
    product_id: int,
    payload: ProductUpdate,
    _: object = Depends(require_roles("Admin", "Manager", "Sales Executive")),
    db: Session = Depends(get_db),
) -> ProductRead:
    """
    Update an existing product.
    """
    product = get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return update_product(db, product, payload)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_route(
    product_id: int,
    _: object = Depends(require_roles("Admin", "Manager")),
    db: Session = Depends(get_db),
) -> None:
    """
    Delete a product record.
    """
    product = get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    delete_product(db, product)
