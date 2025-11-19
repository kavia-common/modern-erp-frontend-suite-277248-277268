"""
Service layer for Purchases business logic.
"""
from typing import Optional
from ..repositories.purchases import purchases_repository
from ..schemas.purchases import PurchaseCreate, PurchaseUpdate, PurchaseResponse
from ..schemas.common import PaginatedResponse
import logging

logger = logging.getLogger(__name__)


class PurchasesService:
    """Service for purchases business logic."""
    
    def __init__(self):
        self.repository = purchases_repository
    
    def create_purchase(self, purchase_data: PurchaseCreate) -> PurchaseResponse:
        """Create a new purchase record."""
        try:
            data = purchase_data.model_dump()
            purchase = self.repository.create(data)
            return PurchaseResponse(**purchase)
        except Exception as e:
            logger.error(f"Error creating purchase: {str(e)}")
            raise
    
    def get_purchase(self, purchase_id: int) -> Optional[PurchaseResponse]:
        """Get a purchase record by ID."""
        purchase = self.repository.get_by_id(purchase_id)
        if purchase:
            return PurchaseResponse(**purchase)
        return None
    
    def get_purchases(
        self,
        skip: int = 0,
        limit: int = 10,
        payment_status: Optional[str] = None,
        delivery_status: Optional[str] = None,
        supplier_name: Optional[str] = None
    ) -> PaginatedResponse[PurchaseResponse]:
        """Get all purchase records with pagination and filtering."""
        filters = {}
        if payment_status:
            filters["payment_status"] = payment_status
        if delivery_status:
            filters["delivery_status"] = delivery_status
        if supplier_name:
            filters["supplier_name"] = supplier_name
        
        purchases = self.repository.get_all(skip=skip, limit=limit, filters=filters)
        total = self.repository.count(filters=filters)
        
        return PaginatedResponse(
            items=[PurchaseResponse(**purchase) for purchase in purchases],
            total=total,
            skip=skip,
            limit=limit
        )
    
    def update_purchase(self, purchase_id: int, purchase_data: PurchaseUpdate) -> Optional[PurchaseResponse]:
        """Update a purchase record."""
        try:
            data = purchase_data.model_dump(exclude_unset=True)
            purchase = self.repository.update(purchase_id, data)
            if purchase:
                return PurchaseResponse(**purchase)
            return None
        except Exception as e:
            logger.error(f"Error updating purchase {purchase_id}: {str(e)}")
            raise
    
    def delete_purchase(self, purchase_id: int) -> bool:
        """Delete a purchase record."""
        return self.repository.delete(purchase_id)


# Singleton instance
purchases_service = PurchasesService()
