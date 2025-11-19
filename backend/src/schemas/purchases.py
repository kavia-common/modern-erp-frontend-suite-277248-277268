"""
Pydantic schemas for Purchases module.
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class PurchaseBase(BaseModel):
    """Base schema for purchases."""
    supplier_name: str = Field(..., min_length=1, max_length=200, description="Supplier name")
    item_name: str = Field(..., min_length=1, max_length=200, description="Item purchased")
    quantity: int = Field(..., ge=1, description="Quantity purchased")
    unit_cost: float = Field(..., ge=0, description="Unit cost")
    total_cost: float = Field(..., ge=0, description="Total purchase cost")
    payment_status: str = Field(default="pending", max_length=50, description="Payment status")
    delivery_status: str = Field(default="pending", max_length=50, description="Delivery status")
    notes: Optional[str] = Field(default=None, max_length=500, description="Additional notes")


class PurchaseCreate(PurchaseBase):
    """Schema for creating a purchase."""
    pass


class PurchaseUpdate(BaseModel):
    """Schema for updating a purchase."""
    supplier_name: Optional[str] = Field(None, min_length=1, max_length=200)
    item_name: Optional[str] = Field(None, min_length=1, max_length=200)
    quantity: Optional[int] = Field(None, ge=1)
    unit_cost: Optional[float] = Field(None, ge=0)
    total_cost: Optional[float] = Field(None, ge=0)
    payment_status: Optional[str] = Field(None, max_length=50)
    delivery_status: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = Field(None, max_length=500)


class PurchaseResponse(PurchaseBase):
    """Schema for purchase response."""
    id: int = Field(..., description="Unique identifier")
    purchase_date: datetime = Field(..., description="Purchase date")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True
