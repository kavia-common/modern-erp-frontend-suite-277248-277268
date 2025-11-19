"""
Repository for Purchases data access.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class PurchasesRepository:
    """Repository for managing purchase records in memory."""
    
    def __init__(self):
        self._data: Dict[int, Dict[str, Any]] = {}
        self._next_id: int = 1
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample data."""
        sample_purchases = [
            {
                "supplier_name": "Tech Supplies Inc",
                "item_name": "Laptop",
                "quantity": 10,
                "unit_cost": 850.00,
                "total_cost": 8500.00,
                "payment_status": "paid",
                "delivery_status": "delivered",
                "notes": "Bulk order discount applied",
                "purchase_date": datetime.utcnow()
            },
            {
                "supplier_name": "Office Furniture Co",
                "item_name": "Office Chair",
                "quantity": 20,
                "unit_cost": 250.00,
                "total_cost": 5000.00,
                "payment_status": "pending",
                "delivery_status": "in_transit",
                "notes": None,
                "purchase_date": datetime.utcnow()
            }
        ]
        
        for purchase in sample_purchases:
            self.create(purchase)
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new purchase record."""
        purchase = {
            "id": self._next_id,
            **data,
            "purchase_date": data.get("purchase_date", datetime.utcnow()),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        self._data[self._next_id] = purchase
        self._next_id += 1
        logger.info(f"Created purchase record with ID: {purchase['id']}")
        return purchase
    
    def get_by_id(self, item_id: int) -> Optional[Dict[str, Any]]:
        """Get a purchase record by ID."""
        return self._data.get(item_id)
    
    def get_all(self, skip: int = 0, limit: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Get all purchase records with pagination and optional filters."""
        purchases = list(self._data.values())
        
        # Apply filters
        if filters:
            if "payment_status" in filters:
                purchases = [p for p in purchases if p.get("payment_status") == filters["payment_status"]]
            if "delivery_status" in filters:
                purchases = [p for p in purchases if p.get("delivery_status") == filters["delivery_status"]]
            if "supplier_name" in filters:
                supplier = filters["supplier_name"].lower()
                purchases = [p for p in purchases if supplier in p.get("supplier_name", "").lower()]
        
        # Sort by purchase_date descending
        purchases.sort(key=lambda x: x.get("purchase_date", datetime.min), reverse=True)
        
        # Apply pagination
        return purchases[skip:skip + limit]
    
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count purchase records with optional filters."""
        purchases = list(self._data.values())
        
        if filters:
            if "payment_status" in filters:
                purchases = [p for p in purchases if p.get("payment_status") == filters["payment_status"]]
            if "delivery_status" in filters:
                purchases = [p for p in purchases if p.get("delivery_status") == filters["delivery_status"]]
            if "supplier_name" in filters:
                supplier = filters["supplier_name"].lower()
                purchases = [p for p in purchases if supplier in p.get("supplier_name", "").lower()]
        
        return len(purchases)
    
    def update(self, item_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a purchase record by ID."""
        if item_id not in self._data:
            return None
        
        # Update only provided fields
        for key, value in data.items():
            if value is not None:
                self._data[item_id][key] = value
        
        self._data[item_id]["updated_at"] = datetime.utcnow()
        logger.info(f"Updated purchase record with ID: {item_id}")
        return self._data[item_id]
    
    def delete(self, item_id: int) -> bool:
        """Delete a purchase record by ID."""
        if item_id in self._data:
            del self._data[item_id]
            logger.info(f"Deleted purchase record with ID: {item_id}")
            return True
        return False


# Singleton instance
purchases_repository = PurchasesRepository()
