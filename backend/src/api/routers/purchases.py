"""
Purchases router for managing purchase records.
"""
from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional
from ...schemas.purchases import PurchaseCreate, PurchaseUpdate, PurchaseResponse
from ...schemas.common import PaginatedResponse, SuccessResponse
from ...services.purchases import purchases_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/purchases", tags=["Purchases"])


# PUBLIC_INTERFACE
@router.post(
    "/",
    response_model=PurchaseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Purchase",
    description="Create a new purchase record"
)
async def create_purchase(purchase: PurchaseCreate):
    """
    Create a new purchase record.
    
    Args:
        purchase: Purchase data
        
    Returns:
        PurchaseResponse: Created purchase record
    """
    try:
        return purchases_service.create_purchase(purchase)
    except Exception as e:
        logger.error(f"Error creating purchase: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create purchase record"
        )


# PUBLIC_INTERFACE
@router.get(
    "/",
    response_model=PaginatedResponse[PurchaseResponse],
    summary="List Purchases",
    description="Retrieve a paginated list of purchase records with optional filtering"
)
async def list_purchases(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return"),
    payment_status: Optional[str] = Query(None, description="Filter by payment status"),
    delivery_status: Optional[str] = Query(None, description="Filter by delivery status"),
    supplier_name: Optional[str] = Query(None, description="Filter by supplier name")
):
    """
    Get a paginated list of purchase records.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        payment_status: Optional payment status filter
        delivery_status: Optional delivery status filter
        supplier_name: Optional supplier name filter
        
    Returns:
        PaginatedResponse: Paginated list of purchase records
    """
    try:
        return purchases_service.get_purchases(
            skip=skip,
            limit=limit,
            payment_status=payment_status,
            delivery_status=delivery_status,
            supplier_name=supplier_name
        )
    except Exception as e:
        logger.error(f"Error listing purchases: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve purchase records"
        )


# PUBLIC_INTERFACE
@router.get(
    "/{purchase_id}",
    response_model=PurchaseResponse,
    summary="Get Purchase",
    description="Retrieve a specific purchase record by ID"
)
async def get_purchase(purchase_id: int):
    """
    Get a purchase record by ID.
    
    Args:
        purchase_id: Purchase ID
        
    Returns:
        PurchaseResponse: Purchase record details
    """
    purchase = purchases_service.get_purchase(purchase_id)
    if not purchase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Purchase with ID {purchase_id} not found"
        )
    return purchase


# PUBLIC_INTERFACE
@router.put(
    "/{purchase_id}",
    response_model=PurchaseResponse,
    summary="Update Purchase",
    description="Update an existing purchase record"
)
async def update_purchase(purchase_id: int, purchase: PurchaseUpdate):
    """
    Update a purchase record.
    
    Args:
        purchase_id: Purchase ID
        purchase: Updated purchase data
        
    Returns:
        PurchaseResponse: Updated purchase record
    """
    try:
        updated_purchase = purchases_service.update_purchase(purchase_id, purchase)
        if not updated_purchase:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Purchase with ID {purchase_id} not found"
            )
        return updated_purchase
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating purchase: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update purchase record"
        )


# PUBLIC_INTERFACE
@router.delete(
    "/{purchase_id}",
    response_model=SuccessResponse,
    summary="Delete Purchase",
    description="Delete a purchase record by ID"
)
async def delete_purchase(purchase_id: int):
    """
    Delete a purchase record.
    
    Args:
        purchase_id: Purchase ID
        
    Returns:
        SuccessResponse: Success message
    """
    if not purchases_service.delete_purchase(purchase_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Purchase with ID {purchase_id} not found"
        )
    return SuccessResponse(message="Purchase record deleted successfully")
