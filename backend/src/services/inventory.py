"""
Service layer for Inventory business logic.
"""
from typing import List, Optional
from ..repositories.inventory import inventory_repository
from ..schemas.inventory import InventoryItemCreate, InventoryItemUpdate, InventoryItemResponse
from ..schemas.common import PaginatedResponse
import logging

logger = logging.getLogger(__name__)


class InventoryService:
    """Service for inventory business logic."""
    
    def __init__(self):
        self.repository = inventory_repository
    
    def create_item(self, item_data: InventoryItemCreate) -> InventoryItemResponse:
        """Create a new inventory item."""
        try:
            data = item_data.model_dump()
            item = self.repository.create(data)
            return InventoryItemResponse(**item)
        except Exception as e:
            logger.error(f"Error creating inventory item: {str(e)}")
            raise
    
    def get_item(self, item_id: int) -> Optional[InventoryItemResponse]:
        """Get an inventory item by ID."""
        item = self.repository.get_by_id(item_id)
        if item:
            return InventoryItemResponse(**item)
        return None
    
    def get_items(
        self,
        skip: int = 0,
        limit: int = 10,
        category: Optional[str] = None,
        search: Optional[str] = None
    ) -> PaginatedResponse[InventoryItemResponse]:
        """Get all inventory items with pagination and filtering."""
        filters = {}
        if category:
            filters["category"] = category
        if search:
            filters["search"] = search
        
        items = self.repository.get_all(skip=skip, limit=limit, filters=filters)
        total = self.repository.count(filters=filters)
        
        return PaginatedResponse(
            items=[InventoryItemResponse(**item) for item in items],
            total=total,
            skip=skip,
            limit=limit
        )
    
    def update_item(self, item_id: int, item_data: InventoryItemUpdate) -> Optional[InventoryItemResponse]:
        """Update an inventory item."""
        try:
            data = item_data.model_dump(exclude_unset=True)
            item = self.repository.update(item_id, data)
            if item:
                return InventoryItemResponse(**item)
            return None
        except Exception as e:
            logger.error(f"Error updating inventory item {item_id}: {str(e)}")
            raise
    
    def delete_item(self, item_id: int) -> bool:
        """Delete an inventory item."""
        return self.repository.delete(item_id)
    
    def get_low_stock_items(self) -> List[InventoryItemResponse]:
        """Get items below reorder level."""
        all_items = self.repository.get_all(skip=0, limit=1000)
        low_stock = [item for item in all_items if item["quantity"] <= item["reorder_level"]]
        return [InventoryItemResponse(**item) for item in low_stock]


# Singleton instance
inventory_service = InventoryService()
