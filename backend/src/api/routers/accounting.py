"""
Accounting router for managing accounting entries.
"""
from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional
from ...schemas.accounting import AccountingEntryCreate, AccountingEntryUpdate, AccountingEntryResponse
from ...schemas.common import PaginatedResponse, SuccessResponse
from ...services.accounting import accounting_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/accounting", tags=["Accounting"])


# PUBLIC_INTERFACE
@router.post(
    "/",
    response_model=AccountingEntryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Accounting Entry",
    description="Create a new accounting entry"
)
async def create_accounting_entry(entry: AccountingEntryCreate):
    """
    Create a new accounting entry.
    
    Args:
        entry: Accounting entry data
        
    Returns:
        AccountingEntryResponse: Created accounting entry
    """
    try:
        return accounting_service.create_entry(entry)
    except Exception as e:
        logger.error(f"Error creating accounting entry: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create accounting entry"
        )


# PUBLIC_INTERFACE
@router.get(
    "/",
    response_model=PaginatedResponse[AccountingEntryResponse],
    summary="List Accounting Entries",
    description="Retrieve a paginated list of accounting entries with optional filtering"
)
async def list_accounting_entries(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return"),
    transaction_type: Optional[str] = Query(None, description="Filter by transaction type (debit/credit)"),
    category: Optional[str] = Query(None, description="Filter by category"),
    account_name: Optional[str] = Query(None, description="Filter by account name")
):
    """
    Get a paginated list of accounting entries.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        transaction_type: Optional transaction type filter
        category: Optional category filter
        account_name: Optional account name filter
        
    Returns:
        PaginatedResponse: Paginated list of accounting entries
    """
    try:
        return accounting_service.get_entries(
            skip=skip,
            limit=limit,
            transaction_type=transaction_type,
            category=category,
            account_name=account_name
        )
    except Exception as e:
        logger.error(f"Error listing accounting entries: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve accounting entries"
        )


# PUBLIC_INTERFACE
@router.get(
    "/{entry_id}",
    response_model=AccountingEntryResponse,
    summary="Get Accounting Entry",
    description="Retrieve a specific accounting entry by ID"
)
async def get_accounting_entry(entry_id: int):
    """
    Get an accounting entry by ID.
    
    Args:
        entry_id: Accounting entry ID
        
    Returns:
        AccountingEntryResponse: Accounting entry details
    """
    entry = accounting_service.get_entry(entry_id)
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Accounting entry with ID {entry_id} not found"
        )
    return entry


# PUBLIC_INTERFACE
@router.put(
    "/{entry_id}",
    response_model=AccountingEntryResponse,
    summary="Update Accounting Entry",
    description="Update an existing accounting entry"
)
async def update_accounting_entry(entry_id: int, entry: AccountingEntryUpdate):
    """
    Update an accounting entry.
    
    Args:
        entry_id: Accounting entry ID
        entry: Updated accounting entry data
        
    Returns:
        AccountingEntryResponse: Updated accounting entry
    """
    try:
        updated_entry = accounting_service.update_entry(entry_id, entry)
        if not updated_entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Accounting entry with ID {entry_id} not found"
            )
        return updated_entry
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating accounting entry: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update accounting entry"
        )


# PUBLIC_INTERFACE
@router.delete(
    "/{entry_id}",
    response_model=SuccessResponse,
    summary="Delete Accounting Entry",
    description="Delete an accounting entry by ID"
)
async def delete_accounting_entry(entry_id: int):
    """
    Delete an accounting entry.
    
    Args:
        entry_id: Accounting entry ID
        
    Returns:
        SuccessResponse: Success message
    """
    if not accounting_service.delete_entry(entry_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Accounting entry with ID {entry_id} not found"
        )
    return SuccessResponse(message="Accounting entry deleted successfully")
