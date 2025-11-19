"""
Repository for Inventory data access.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class InventoryRepository:
    """Repository for managing inventory items in memory."""
    
    def __init__(self):
        self._data: Dict[int, Dict[str, Any]] = {}
        self._next_id: int = 1
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample data."""
        sample_items = [
            {
                "name": "Laptop",
                "sku": "TECH-001",
                "category": "Electronics",
                "quantity": 50,
                "unit_price": 999.99,
                "reorder_level": 10,
                "description": "High-performance laptop"
            },
            {
                "name": "Office Chair",
                "sku": "FURN-001",
                "category": "Furniture",
                "quantity": 25,
                "unit_price": 299.99,
                "reorder_level": 5,
                "description": "Ergonomic office chair"
            },
            {
                "name": "Notebook",
                "sku": "STAT-001",
                "category": "Stationery",
                "quantity": 200,
                "unit_price": 4.99,
                "reorder_level": 50,
                "description": "A4 ruled notebook"
            }
        ]
        
        for item in sample_items:
            self.create(item)
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new inventory item."""
        item = {
            "id": self._next_id,
            **data,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        self._data[self._next_id] = item
        self._next_id += 1
        logger.info(f"Created inventory item with ID: {item['id']}")
        return item
    
    def get_by_id(self, item_id: int) -> Optional[Dict[str, Any]]:
        """Get an inventory item by ID."""
        return self._data.get(item_id)
    
    def get_all(self, skip: int = 0, limit: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Get all inventory items with pagination and optional filters."""
        items = list(self._data.values())
        
        # Apply filters
        if filters:
            if "category" in filters:
                items = [item for item in items if item.get("category") == filters["category"]]
            if "search" in filters:
                search_term = filters["search"].lower()
                items = [
                    item for item in items
                    if search_term in item.get("name", "").lower() or
                    search_term in item.get("sku", "").lower()
                ]
        
        # Apply pagination
        return items[skip:skip + limit]
    
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count inventory items with optional filters."""
        items = list(self._data.values())
        
        if filters:
            if "category" in filters:
                items = [item for item in items if item.get("category") == filters["category"]]
            if "search" in filters:
                search_term = filters["search"].lower()
                items = [
                    item for item in items
                    if search_term in item.get("name", "").lower() or
                    search_term in item.get("sku", "").lower()
                ]
        
        return len(items)
    
    def update(self, item_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an inventory item by ID."""
        if item_id not in self._data:
            return None
        
        # Update only provided fields
        for key, value in data.items():
            if value is not None:
                self._data[item_id][key] = value
        
        self._data[item_id]["updated_at"] = datetime.utcnow()
        logger.info(f"Updated inventory item with ID: {item_id}")
        return self._data[item_id]
    
    def delete(self, item_id: int) -> bool:
        """Delete an inventory item by ID."""
        if item_id in self._data:
            del self._data[item_id]
            logger.info(f"Deleted inventory item with ID: {item_id}")
            return True
        return False


# Singleton instance
inventory_repository = InventoryRepository()
