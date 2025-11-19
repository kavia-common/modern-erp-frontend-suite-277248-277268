"""
Pydantic schemas for Sales module.
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class SaleBase(BaseModel):
    """Base schema for sales."""
    customer_name: str = Field(..., min_length=1, max_length=200, description="Customer name")
    item_name: str = Field(..., min_length=1, max_length=200, description="Item sold")
    quantity: int = Field(..., ge=1, description="Quantity sold")
    unit_price: float = Field(..., ge=0, description="Unit price")
    total_amount: float = Field(..., ge=0, description="Total sale amount")
    payment_method: str = Field(..., min_length=1, max_length=50, description="Payment method")
    status: str = Field(default="completed", max_length=50, description="Sale status")
    notes: Optional[str] = Field(default=None, max_length=500, description="Additional notes")


class SaleCreate(SaleBase):
    """Schema for creating a sale."""
    pass


class SaleUpdate(BaseModel):
    """Schema for updating a sale."""
    customer_name: Optional[str] = Field(None, min_length=1, max_length=200)
    item_name: Optional[str] = Field(None, min_length=1, max_length=200)
    quantity: Optional[int] = Field(None, ge=1)
    unit_price: Optional[float] = Field(None, ge=0)
    total_amount: Optional[float] = Field(None, ge=0)
    payment_method: Optional[str] = Field(None, min_length=1, max_length=50)
    status: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = Field(None, max_length=500)


class SaleResponse(SaleBase):
    """Schema for sale response."""
    id: int = Field(..., description="Unique identifier")
    sale_date: datetime = Field(..., description="Sale date")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True
