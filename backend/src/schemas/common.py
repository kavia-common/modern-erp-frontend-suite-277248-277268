"""
Common Pydantic schemas used across the application.
"""
from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel, Field


T = TypeVar('T')


class PaginationParams(BaseModel):
    """Pagination request parameters."""
    skip: int = Field(default=0, ge=0, description="Number of records to skip")
    limit: int = Field(default=10, ge=1, le=100, description="Maximum number of records to return")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper."""
    items: List[T] = Field(description="List of items")
    total: int = Field(description="Total count of items")
    skip: int = Field(description="Number of records skipped")
    limit: int = Field(description="Maximum number of records returned")


class ErrorResponse(BaseModel):
    """Standard error response."""
    detail: str = Field(description="Error message")
    error_code: Optional[str] = Field(default=None, description="Machine-readable error code")


class SuccessResponse(BaseModel):
    """Standard success response."""
    message: str = Field(description="Success message")
    data: Optional[dict] = Field(default=None, description="Optional additional data")
