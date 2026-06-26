from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class ProductCreate(BaseModel):
    sku: str = Field(..., min_length=1, max_length=100, description="Unique stock-keeping unit identifier")
    name: str = Field(..., min_length=1, max_length=255, description="Product name")
    description: Optional[str] = Field(None, max_length=5000, description="Product description")
    price: float = Field(..., gt=0, description="Product price (must be greater than 0)")
    currency: str = Field("USD", min_length=3, max_length=3, description="ISO 4217 currency code")
    inventory_count: int = Field(0, ge=0, description="Available inventory quantity")
    category: Optional[str] = Field(None, max_length=100, description="Product category")
    weight_kg: Optional[float] = Field(None, gt=0, description="Weight in kilograms")
    dimensions: Optional[str] = Field(None, max_length=100, description="Dimensions (e.g. 10x20x5 cm)")
    brand: Optional[str] = Field(None, max_length=100, description="Brand name")
    is_active: bool = Field(True, description="Whether the product is active in the catalogue")

    @field_validator("sku", "name")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Must not be blank or whitespace-only")
        return v.strip()

    @field_validator("currency")
    @classmethod
    def uppercase_currency(cls, v: str) -> str:
        return v.upper()


class ProductUpdate(BaseModel):
    sku: Optional[str] = Field(None, min_length=1, max_length=100)
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)
    price: Optional[float] = Field(None, gt=0)
    currency: Optional[str] = Field(None, min_length=3, max_length=3)
    inventory_count: Optional[int] = Field(None, ge=0)
    category: Optional[str] = Field(None, max_length=100)
    weight_kg: Optional[float] = Field(None, gt=0)
    dimensions: Optional[str] = Field(None, max_length=100)
    brand: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None

    @field_validator("sku", "name")
    @classmethod
    def not_blank(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Must not be blank or whitespace-only")
        return v.strip() if v else v

    @field_validator("currency")
    @classmethod
    def uppercase_currency(cls, v):
        return v.upper() if v else v


class ProductResponse(BaseModel):
    id: int
    sku: str
    name: str
    description: Optional[str]
    price: float
    currency: str
    inventory_count: int
    category: Optional[str]
    weight_kg: Optional[float]
    dimensions: Optional[str]
    brand: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    detail: str
