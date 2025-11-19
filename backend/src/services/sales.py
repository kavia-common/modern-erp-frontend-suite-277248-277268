"""
Service layer for Sales business logic.
"""
from typing import Optional
from ..repositories.sales import sales_repository
from ..schemas.sales import SaleCreate, SaleUpdate, SaleResponse
from ..schemas.common import PaginatedResponse
import logging

logger = logging.getLogger(__name__)


class SalesService:
    """Service for sales business logic."""
    
    def __init__(self):
        self.repository = sales_repository
    
    def create_sale(self, sale_data: SaleCreate) -> SaleResponse:
        """Create a new sale record."""
        try:
            data = sale_data.model_dump()
            sale = self.repository.create(data)
            return SaleResponse(**sale)
        except Exception as e:
            logger.error(f"Error creating sale: {str(e)}")
            raise
    
    def get_sale(self, sale_id: int) -> Optional[SaleResponse]:
        """Get a sale record by ID."""
        sale = self.repository.get_by_id(sale_id)
        if sale:
            return SaleResponse(**sale)
        return None
    
    def get_sales(
        self,
        skip: int = 0,
        limit: int = 10,
        status: Optional[str] = None,
        customer_name: Optional[str] = None
    ) -> PaginatedResponse[SaleResponse]:
        """Get all sale records with pagination and filtering."""
        filters = {}
        if status:
            filters["status"] = status
        if customer_name:
            filters["customer_name"] = customer_name
        
        sales = self.repository.get_all(skip=skip, limit=limit, filters=filters)
        total = self.repository.count(filters=filters)
        
        return PaginatedResponse(
            items=[SaleResponse(**sale) for sale in sales],
            total=total,
            skip=skip,
            limit=limit
        )
    
    def update_sale(self, sale_id: int, sale_data: SaleUpdate) -> Optional[SaleResponse]:
        """Update a sale record."""
        try:
            data = sale_data.model_dump(exclude_unset=True)
            sale = self.repository.update(sale_id, data)
            if sale:
                return SaleResponse(**sale)
            return None
        except Exception as e:
            logger.error(f"Error updating sale {sale_id}: {str(e)}")
            raise
    
    def delete_sale(self, sale_id: int) -> bool:
        """Delete a sale record."""
        return self.repository.delete(sale_id)


# Singleton instance
sales_service = SalesService()
