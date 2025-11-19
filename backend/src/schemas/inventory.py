"""
Pydantic schemas for Inventory module.
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class InventoryItemBase(BaseModel):
    """Base schema for inventory items."""
    name: str = Field(..., min_length=1, max_length=200, description="Item name")
    sku: str = Field(..., min_length=1, max_length=100, description="Stock Keeping Unit")
    category: str = Field(..., min_length=1, max_length=100, description="Item category")
    quantity: int = Field(..., ge=0, description="Quantity in stock")
    unit_price: float = Field(..., ge=0, description="Unit price")
    reorder_level: int = Field(default=10, ge=0, description="Reorder threshold")
    description: Optional[str] = Field(default=None, max_length=500, description="Item description")


class InventoryItemCreate(InventoryItemBase):
    """Schema for creating an inventory item."""
    pass


class InventoryItemUpdate(BaseModel):
    """Schema for updating an inventory item."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    sku: Optional[str] = Field(None, min_length=1, max_length=100)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    quantity: Optional[int] = Field(None, ge=0)
    unit_price: Optional[float] = Field(None, ge=0)
    reorder_level: Optional[int] = Field(None, ge=0)
    description: Optional[str] = Field(None, max_length=500)


class InventoryItemResponse(InventoryItemBase):
    """Schema for inventory item response."""
    id: int = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True
