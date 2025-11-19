"""
Service layer for HR business logic.
"""
from typing import Optional
from ..repositories.hr import hr_repository
from ..schemas.hr import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from ..schemas.common import PaginatedResponse
import logging

logger = logging.getLogger(__name__)


class HRService:
    """Service for HR business logic."""
    
    def __init__(self):
        self.repository = hr_repository
    
    def create_employee(self, employee_data: EmployeeCreate) -> EmployeeResponse:
        """Create a new employee record."""
        try:
            data = employee_data.model_dump()
            employee = self.repository.create(data)
            return EmployeeResponse(**employee)
        except Exception as e:
            logger.error(f"Error creating employee: {str(e)}")
            raise
    
    def get_employee(self, employee_id: int) -> Optional[EmployeeResponse]:
        """Get an employee record by ID."""
        employee = self.repository.get_by_id(employee_id)
        if employee:
            return EmployeeResponse(**employee)
        return None
    
    def get_employees(
        self,
        skip: int = 0,
        limit: int = 10,
        department: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None
    ) -> PaginatedResponse[EmployeeResponse]:
        """Get all employee records with pagination and filtering."""
        filters = {}
        if department:
            filters["department"] = department
        if status:
            filters["status"] = status
        if search:
            filters["search"] = search
        
        employees = self.repository.get_all(skip=skip, limit=limit, filters=filters)
        total = self.repository.count(filters=filters)
        
        return PaginatedResponse(
            items=[EmployeeResponse(**employee) for employee in employees],
            total=total,
            skip=skip,
            limit=limit
        )
    
    def update_employee(self, employee_id: int, employee_data: EmployeeUpdate) -> Optional[EmployeeResponse]:
        """Update an employee record."""
        try:
            data = employee_data.model_dump(exclude_unset=True)
            employee = self.repository.update(employee_id, data)
            if employee:
                return EmployeeResponse(**employee)
            return None
        except Exception as e:
            logger.error(f"Error updating employee {employee_id}: {str(e)}")
            raise
    
    def delete_employee(self, employee_id: int) -> bool:
        """Delete an employee record."""
        return self.repository.delete(employee_id)


# Singleton instance
hr_service = HRService()
