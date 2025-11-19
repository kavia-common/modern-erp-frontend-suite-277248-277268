"""
Pydantic schemas for HR module.
"""
from typing import Optional
from datetime import datetime, date
from pydantic import BaseModel, Field, EmailStr


class EmployeeBase(BaseModel):
    """Base schema for employees."""
    first_name: str = Field(..., min_length=1, max_length=100, description="First name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Last name")
    email: EmailStr = Field(..., description="Email address")
    phone: Optional[str] = Field(default=None, max_length=20, description="Phone number")
    department: str = Field(..., min_length=1, max_length=100, description="Department")
    position: str = Field(..., min_length=1, max_length=100, description="Job position")
    salary: float = Field(..., ge=0, description="Annual salary")
    hire_date: date = Field(..., description="Hire date")
    status: str = Field(default="active", max_length=50, description="Employment status")
    address: Optional[str] = Field(default=None, max_length=500, description="Address")


class EmployeeCreate(EmployeeBase):
    """Schema for creating an employee."""
    pass


class EmployeeUpdate(BaseModel):
    """Schema for updating an employee."""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    department: Optional[str] = Field(None, min_length=1, max_length=100)
    position: Optional[str] = Field(None, min_length=1, max_length=100)
    salary: Optional[float] = Field(None, ge=0)
    hire_date: Optional[date] = None
    status: Optional[str] = Field(None, max_length=50)
    address: Optional[str] = Field(None, max_length=500)


class EmployeeResponse(EmployeeBase):
    """Schema for employee response."""
    id: int = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True
