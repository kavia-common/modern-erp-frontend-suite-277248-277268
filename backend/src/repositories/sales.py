"""
Repository for Sales data access.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class SalesRepository:
    """Repository for managing sales records in memory."""
    
    def __init__(self):
        self._data: Dict[int, Dict[str, Any]] = {}
        self._next_id: int = 1
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample data."""
        sample_sales = [
            {
                "customer_name": "John Doe",
                "item_name": "Laptop",
                "quantity": 2,
                "unit_price": 999.99,
                "total_amount": 1999.98,
                "payment_method": "Credit Card",
                "status": "completed",
                "notes": "Express delivery requested",
                "sale_date": datetime.utcnow()
            },
            {
                "customer_name": "Jane Smith",
                "item_name": "Office Chair",
                "quantity": 5,
                "unit_price": 299.99,
                "total_amount": 1499.95,
                "payment_method": "Bank Transfer",
                "status": "completed",
                "notes": None,
                "sale_date": datetime.utcnow()
            }
        ]
        
        for sale in sample_sales:
            self.create(sale)
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new sale record."""
        sale = {
            "id": self._next_id,
            **data,
            "sale_date": data.get("sale_date", datetime.utcnow()),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        self._data[self._next_id] = sale
        self._next_id += 1
        logger.info(f"Created sale record with ID: {sale['id']}")
        return sale
    
    def get_by_id(self, item_id: int) -> Optional[Dict[str, Any]]:
        """Get a sale record by ID."""
        return self._data.get(item_id)
    
    def get_all(self, skip: int = 0, limit: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Get all sale records with pagination and optional filters."""
        sales = list(self._data.values())
        
        # Apply filters
        if filters:
            if "status" in filters:
                sales = [sale for sale in sales if sale.get("status") == filters["status"]]
            if "customer_name" in filters:
                customer = filters["customer_name"].lower()
                sales = [sale for sale in sales if customer in sale.get("customer_name", "").lower()]
        
        # Sort by sale_date descending
        sales.sort(key=lambda x: x.get("sale_date", datetime.min), reverse=True)
        
        # Apply pagination
        return sales[skip:skip + limit]
    
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count sale records with optional filters."""
        sales = list(self._data.values())
        
        if filters:
            if "status" in filters:
                sales = [sale for sale in sales if sale.get("status") == filters["status"]]
            if "customer_name" in filters:
                customer = filters["customer_name"].lower()
                sales = [sale for sale in sales if customer in sale.get("customer_name", "").lower()]
        
        return len(sales)
    
    def update(self, item_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a sale record by ID."""
        if item_id not in self._data:
            return None
        
        # Update only provided fields
        for key, value in data.items():
            if value is not None:
                self._data[item_id][key] = value
        
        self._data[item_id]["updated_at"] = datetime.utcnow()
        logger.info(f"Updated sale record with ID: {item_id}")
        return self._data[item_id]
    
    def delete(self, item_id: int) -> bool:
        """Delete a sale record by ID."""
        if item_id in self._data:
            del self._data[item_id]
            logger.info(f"Deleted sale record with ID: {item_id}")
            return True
        return False


# Singleton instance
sales_repository = SalesRepository()
