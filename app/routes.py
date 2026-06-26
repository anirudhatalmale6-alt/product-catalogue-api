from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.auth import verify_api_key
from app.database import get_db
from app.models import Product
from app.schemas import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    MessageResponse,
)

router = APIRouter(prefix="/products", tags=["Products"])


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product",
    responses={
        401: {"description": "Invalid or missing API key"},
        409: {"description": "A product with this SKU already exists"},
        422: {"description": "Validation error"},
    },
)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    try:
        db.commit()
        db.refresh(db_product)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A product with SKU '{product.sku}' already exists.",
        )
    return db_product


@router.get(
    "",
    response_model=list[ProductResponse],
    summary="List all products",
    responses={401: {"description": "Invalid or missing API key"}},
)
def list_products(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=200, description="Max records to return"),
    category: Optional[str] = Query(None, description="Filter by category"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    query = db.query(Product)
    if category:
        query = query.filter(Product.category == category)
    if is_active is not None:
        query = query.filter(Product.is_active == int(is_active))
    return query.offset(skip).limit(limit).all()


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Get a product by ID",
    responses={
        401: {"description": "Invalid or missing API key"},
        404: {"description": "Product not found"},
    },
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found.",
        )
    return product


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Update a product",
    responses={
        401: {"description": "Invalid or missing API key"},
        404: {"description": "Product not found"},
        409: {"description": "A product with this SKU already exists"},
        422: {"description": "Validation error"},
    },
)
def update_product(
    product_id: int,
    updates: ProductUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found.",
        )

    update_data = updates.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No fields provided for update.",
        )

    for field, value in update_data.items():
        setattr(product, field, value)

    try:
        db.commit()
        db.refresh(product)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A product with SKU '{updates.sku}' already exists.",
        )
    return product


@router.delete(
    "/{product_id}",
    response_model=MessageResponse,
    summary="Delete a product",
    responses={
        401: {"description": "Invalid or missing API key"},
        404: {"description": "Product not found"},
    },
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found.",
        )
    db.delete(product)
    db.commit()
    return MessageResponse(message=f"Product with id {product_id} has been deleted.")
