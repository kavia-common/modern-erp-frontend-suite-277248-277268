"""
Service layer for Accounting business logic.
"""
from typing import Optional
from ..repositories.accounting import accounting_repository
from ..schemas.accounting import AccountingEntryCreate, AccountingEntryUpdate, AccountingEntryResponse
from ..schemas.common import PaginatedResponse
import logging

logger = logging.getLogger(__name__)


class AccountingService:
    """Service for accounting business logic."""
    
    def __init__(self):
        self.repository = accounting_repository
    
    def create_entry(self, entry_data: AccountingEntryCreate) -> AccountingEntryResponse:
        """Create a new accounting entry."""
        try:
            data = entry_data.model_dump()
            entry = self.repository.create(data)
            return AccountingEntryResponse(**entry)
        except Exception as e:
            logger.error(f"Error creating accounting entry: {str(e)}")
            raise
    
    def get_entry(self, entry_id: int) -> Optional[AccountingEntryResponse]:
        """Get an accounting entry by ID."""
        entry = self.repository.get_by_id(entry_id)
        if entry:
            return AccountingEntryResponse(**entry)
        return None
    
    def get_entries(
        self,
        skip: int = 0,
        limit: int = 10,
        transaction_type: Optional[str] = None,
        category: Optional[str] = None,
        account_name: Optional[str] = None
    ) -> PaginatedResponse[AccountingEntryResponse]:
        """Get all accounting entries with pagination and filtering."""
        filters = {}
        if transaction_type:
            filters["transaction_type"] = transaction_type
        if category:
            filters["category"] = category
        if account_name:
            filters["account_name"] = account_name
        
        entries = self.repository.get_all(skip=skip, limit=limit, filters=filters)
        total = self.repository.count(filters=filters)
        
        return PaginatedResponse(
            items=[AccountingEntryResponse(**entry) for entry in entries],
            total=total,
            skip=skip,
            limit=limit
        )
    
    def update_entry(self, entry_id: int, entry_data: AccountingEntryUpdate) -> Optional[AccountingEntryResponse]:
        """Update an accounting entry."""
        try:
            data = entry_data.model_dump(exclude_unset=True)
            entry = self.repository.update(entry_id, data)
            if entry:
                return AccountingEntryResponse(**entry)
            return None
        except Exception as e:
            logger.error(f"Error updating accounting entry {entry_id}: {str(e)}")
            raise
    
    def delete_entry(self, entry_id: int) -> bool:
        """Delete an accounting entry."""
        return self.repository.delete(entry_id)


# Singleton instance
accounting_service = AccountingService()
