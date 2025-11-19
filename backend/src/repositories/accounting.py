"""
Repository for Accounting data access.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class AccountingRepository:
    """Repository for managing accounting entries in memory."""
    
    def __init__(self):
        self._data: Dict[int, Dict[str, Any]] = {}
        self._next_id: int = 1
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample data."""
        sample_entries = [
            {
                "transaction_type": "credit",
                "account_name": "Sales Revenue",
                "amount": 1999.98,
                "category": "Revenue",
                "reference": "INV-001",
                "description": "Sale of laptops",
                "transaction_date": datetime.utcnow()
            },
            {
                "transaction_type": "debit",
                "account_name": "Purchases",
                "amount": 8500.00,
                "category": "Expense",
                "reference": "PO-001",
                "description": "Purchase of laptops from supplier",
                "transaction_date": datetime.utcnow()
            },
            {
                "transaction_type": "debit",
                "account_name": "Salaries",
                "amount": 5000.00,
                "category": "Expense",
                "reference": "SAL-001",
                "description": "Monthly salary payments",
                "transaction_date": datetime.utcnow()
            }
        ]
        
        for entry in sample_entries:
            self.create(entry)
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new accounting entry."""
        entry = {
            "id": self._next_id,
            **data,
            "transaction_date": data.get("transaction_date", datetime.utcnow()),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        self._data[self._next_id] = entry
        self._next_id += 1
        logger.info(f"Created accounting entry with ID: {entry['id']}")
        return entry
    
    def get_by_id(self, item_id: int) -> Optional[Dict[str, Any]]:
        """Get an accounting entry by ID."""
        return self._data.get(item_id)
    
    def get_all(self, skip: int = 0, limit: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Get all accounting entries with pagination and optional filters."""
        entries = list(self._data.values())
        
        # Apply filters
        if filters:
            if "transaction_type" in filters:
                entries = [e for e in entries if e.get("transaction_type") == filters["transaction_type"]]
            if "category" in filters:
                entries = [e for e in entries if e.get("category") == filters["category"]]
            if "account_name" in filters:
                account = filters["account_name"].lower()
                entries = [e for e in entries if account in e.get("account_name", "").lower()]
        
        # Sort by transaction_date descending
        entries.sort(key=lambda x: x.get("transaction_date", datetime.min), reverse=True)
        
        # Apply pagination
        return entries[skip:skip + limit]
    
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count accounting entries with optional filters."""
        entries = list(self._data.values())
        
        if filters:
            if "transaction_type" in filters:
                entries = [e for e in entries if e.get("transaction_type") == filters["transaction_type"]]
            if "category" in filters:
                entries = [e for e in entries if e.get("category") == filters["category"]]
            if "account_name" in filters:
                account = filters["account_name"].lower()
                entries = [e for e in entries if account in e.get("account_name", "").lower()]
        
        return len(entries)
    
    def update(self, item_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an accounting entry by ID."""
        if item_id not in self._data:
            return None
        
        # Update only provided fields
        for key, value in data.items():
            if value is not None:
                self._data[item_id][key] = value
        
        self._data[item_id]["updated_at"] = datetime.utcnow()
        logger.info(f"Updated accounting entry with ID: {item_id}")
        return self._data[item_id]
    
    def delete(self, item_id: int) -> bool:
        """Delete an accounting entry by ID."""
        if item_id in self._data:
            del self._data[item_id]
            logger.info(f"Deleted accounting entry with ID: {item_id}")
            return True
        return False


# Singleton instance
accounting_repository = AccountingRepository()
