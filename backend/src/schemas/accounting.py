"""
Pydantic schemas for Accounting module.
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class AccountingEntryBase(BaseModel):
    """Base schema for accounting entries."""
    transaction_type: str = Field(..., min_length=1, max_length=50, description="Transaction type (debit/credit)")
    account_name: str = Field(..., min_length=1, max_length=200, description="Account name")
    amount: float = Field(..., gt=0, description="Transaction amount")
    category: str = Field(..., min_length=1, max_length=100, description="Transaction category")
    reference: Optional[str] = Field(default=None, max_length=100, description="Reference number")
    description: Optional[str] = Field(default=None, max_length=500, description="Transaction description")


class AccountingEntryCreate(AccountingEntryBase):
    """Schema for creating an accounting entry."""
    pass


class AccountingEntryUpdate(BaseModel):
    """Schema for updating an accounting entry."""
    transaction_type: Optional[str] = Field(None, min_length=1, max_length=50)
    account_name: Optional[str] = Field(None, min_length=1, max_length=200)
    amount: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    reference: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class AccountingEntryResponse(AccountingEntryBase):
    """Schema for accounting entry response."""
    id: int = Field(..., description="Unique identifier")
    transaction_date: datetime = Field(..., description="Transaction date")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True
