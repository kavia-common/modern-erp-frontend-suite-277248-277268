"""
Inventory router for managing inventory items.
"""
from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional
from ...schemas.inventory import InventoryItemCreate, InventoryItemUpdate, InventoryItemResponse
from ...schemas.common import PaginatedResponse, SuccessResponse
from ...services.inventory import inventory_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/inventory", tags=["Inventory"])


# PUBLIC_INTERFACE
@router.post(
    "/",
    response_model=InventoryItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Inventory Item",
    description="Create a new inventory item with the provided details"
)
async def create_inventory_item(item: InventoryItemCreate):
    """
    Create a new inventory item.
    
    Args:
        item: Inventory item data
        
    Returns:
        InventoryItemResponse: Created inventory item
    """
    try:
        return inventory_service.create_item(item)
    except Exception as e:
        logger.error(f"Error creating inventory item: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create inventory item"
        )


# PUBLIC_INTERFACE
@router.get(
    "/",
    response_model=PaginatedResponse[InventoryItemResponse],
    summary="List Inventory Items",
    description="Retrieve a paginated list of inventory items with optional filtering"
)
async def list_inventory_items(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return"),
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search by name or SKU")
):
    """
    Get a paginated list of inventory items.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        category: Optional category filter
        search: Optional search term
        
    Returns:
        PaginatedResponse: Paginated list of inventory items
    """
    try:
        return inventory_service.get_items(skip=skip, limit=limit, category=category, search=search)
    except Exception as e:
        logger.error(f"Error listing inventory items: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve inventory items"
        )


# PUBLIC_INTERFACE
@router.get(
    "/{item_id}",
    response_model=InventoryItemResponse,
    summary="Get Inventory Item",
    description="Retrieve a specific inventory item by ID"
)
async def get_inventory_item(item_id: int):
    """
    Get an inventory item by ID.
    
    Args:
        item_id: Inventory item ID
        
    Returns:
        InventoryItemResponse: Inventory item details
    """
    item = inventory_service.get_item(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory item with ID {item_id} not found"
        )
    return item


# PUBLIC_INTERFACE
@router.put(
    "/{item_id}",
    response_model=InventoryItemResponse,
    summary="Update Inventory Item",
    description="Update an existing inventory item"
)
async def update_inventory_item(item_id: int, item: InventoryItemUpdate):
    """
    Update an inventory item.
    
    Args:
        item_id: Inventory item ID
        item: Updated inventory item data
        
    Returns:
        InventoryItemResponse: Updated inventory item
    """
    try:
        updated_item = inventory_service.update_item(item_id, item)
        if not updated_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Inventory item with ID {item_id} not found"
            )
        return updated_item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating inventory item: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update inventory item"
        )


# PUBLIC_INTERFACE
@router.delete(
    "/{item_id}",
    response_model=SuccessResponse,
    summary="Delete Inventory Item",
    description="Delete an inventory item by ID"
)
async def delete_inventory_item(item_id: int):
    """
    Delete an inventory item.
    
    Args:
        item_id: Inventory item ID
        
    Returns:
        SuccessResponse: Success message
    """
    if not inventory_service.delete_item(item_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory item with ID {item_id} not found"
        )
    return SuccessResponse(message="Inventory item deleted successfully")
