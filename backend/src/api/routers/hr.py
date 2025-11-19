"""
HR router for managing employee records.
"""
from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional
from ...schemas.hr import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from ...schemas.common import PaginatedResponse, SuccessResponse
from ...services.hr import hr_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/hr", tags=["HR"])


# PUBLIC_INTERFACE
@router.post(
    "/employees",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Employee",
    description="Create a new employee record"
)
async def create_employee(employee: EmployeeCreate):
    """
    Create a new employee record.
    
    Args:
        employee: Employee data
        
    Returns:
        EmployeeResponse: Created employee record
    """
    try:
        return hr_service.create_employee(employee)
    except Exception as e:
        logger.error(f"Error creating employee: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create employee record"
        )


# PUBLIC_INTERFACE
@router.get(
    "/employees",
    response_model=PaginatedResponse[EmployeeResponse],
    summary="List Employees",
    description="Retrieve a paginated list of employee records with optional filtering"
)
async def list_employees(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return"),
    department: Optional[str] = Query(None, description="Filter by department"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status"),
    search: Optional[str] = Query(None, description="Search by name or email")
):
    """
    Get a paginated list of employee records.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        department: Optional department filter
        status_filter: Optional status filter
        search: Optional search term
        
    Returns:
        PaginatedResponse: Paginated list of employee records
    """
    try:
        return hr_service.get_employees(
            skip=skip,
            limit=limit,
            department=department,
            status=status_filter,
            search=search
        )
    except Exception as e:
        logger.error(f"Error listing employees: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve employee records"
        )


# PUBLIC_INTERFACE
@router.get(
    "/employees/{employee_id}",
    response_model=EmployeeResponse,
    summary="Get Employee",
    description="Retrieve a specific employee record by ID"
)
async def get_employee(employee_id: int):
    """
    Get an employee record by ID.
    
    Args:
        employee_id: Employee ID
        
    Returns:
        EmployeeResponse: Employee record details
    """
    employee = hr_service.get_employee(employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {employee_id} not found"
        )
    return employee


# PUBLIC_INTERFACE
@router.put(
    "/employees/{employee_id}",
    response_model=EmployeeResponse,
    summary="Update Employee",
    description="Update an existing employee record"
)
async def update_employee(employee_id: int, employee: EmployeeUpdate):
    """
    Update an employee record.
    
    Args:
        employee_id: Employee ID
        employee: Updated employee data
        
    Returns:
        EmployeeResponse: Updated employee record
    """
    try:
        updated_employee = hr_service.update_employee(employee_id, employee)
        if not updated_employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID {employee_id} not found"
            )
        return updated_employee
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating employee: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update employee record"
        )


# PUBLIC_INTERFACE
@router.delete(
    "/employees/{employee_id}",
    response_model=SuccessResponse,
    summary="Delete Employee",
    description="Delete an employee record by ID"
)
async def delete_employee(employee_id: int):
    """
    Delete an employee record.
    
    Args:
        employee_id: Employee ID
        
    Returns:
        SuccessResponse: Success message
    """
    if not hr_service.delete_employee(employee_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {employee_id} not found"
        )
    return SuccessResponse(message="Employee record deleted successfully")
