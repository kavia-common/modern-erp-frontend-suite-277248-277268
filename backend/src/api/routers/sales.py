"""
Sales router for managing sales records.
"""
from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional
from ...schemas.sales import SaleCreate, SaleUpdate, SaleResponse
from ...schemas.common import PaginatedResponse, SuccessResponse
from ...services.sales import sales_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/sales", tags=["Sales"])


# PUBLIC_INTERFACE
@router.post(
    "/",
    response_model=SaleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Sale",
    description="Create a new sale record"
)
async def create_sale(sale: SaleCreate):
    """
    Create a new sale record.
    
    Args:
        sale: Sale data
        
    Returns:
        SaleResponse: Created sale record
    """
    try:
        return sales_service.create_sale(sale)
    except Exception as e:
        logger.error(f"Error creating sale: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create sale record"
        )


# PUBLIC_INTERFACE
@router.get(
    "/",
    response_model=PaginatedResponse[SaleResponse],
    summary="List Sales",
    description="Retrieve a paginated list of sales records with optional filtering"
)
async def list_sales(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status"),
    customer_name: Optional[str] = Query(None, description="Filter by customer name")
):
    """
    Get a paginated list of sales records.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        status_filter: Optional status filter
        customer_name: Optional customer name filter
        
    Returns:
        PaginatedResponse: Paginated list of sales records
    """
    try:
        return sales_service.get_sales(skip=skip, limit=limit, status=status_filter, customer_name=customer_name)
    except Exception as e:
        logger.error(f"Error listing sales: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve sales records"
        )


# PUBLIC_INTERFACE
@router.get(
    "/{sale_id}",
    response_model=SaleResponse,
    summary="Get Sale",
    description="Retrieve a specific sale record by ID"
)
async def get_sale(sale_id: int):
    """
    Get a sale record by ID.
    
    Args:
        sale_id: Sale ID
        
    Returns:
        SaleResponse: Sale record details
    """
    sale = sales_service.get_sale(sale_id)
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sale with ID {sale_id} not found"
        )
    return sale


# PUBLIC_INTERFACE
@router.put(
    "/{sale_id}",
    response_model=SaleResponse,
    summary="Update Sale",
    description="Update an existing sale record"
)
async def update_sale(sale_id: int, sale: SaleUpdate):
    """
    Update a sale record.
    
    Args:
        sale_id: Sale ID
        sale: Updated sale data
        
    Returns:
        SaleResponse: Updated sale record
    """
    try:
        updated_sale = sales_service.update_sale(sale_id, sale)
        if not updated_sale:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sale with ID {sale_id} not found"
            )
        return updated_sale
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating sale: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update sale record"
        )


# PUBLIC_INTERFACE
@router.delete(
    "/{sale_id}",
    response_model=SuccessResponse,
    summary="Delete Sale",
    description="Delete a sale record by ID"
)
async def delete_sale(sale_id: int):
    """
    Delete a sale record.
    
    Args:
        sale_id: Sale ID
        
    Returns:
        SuccessResponse: Success message
    """
    if not sales_service.delete_sale(sale_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sale with ID {sale_id} not found"
        )
    return SuccessResponse(message="Sale record deleted successfully")
