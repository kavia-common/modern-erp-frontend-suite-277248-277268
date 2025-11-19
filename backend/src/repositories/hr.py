"""
Repository for HR data access.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)


class HRRepository:
    """Repository for managing employee records in memory."""
    
    def __init__(self):
        self._data: Dict[int, Dict[str, Any]] = {}
        self._next_id: int = 1
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample data."""
        sample_employees = [
            {
                "first_name": "Alice",
                "last_name": "Johnson",
                "email": "alice.johnson@example.com",
                "phone": "+1-555-0101",
                "department": "Engineering",
                "position": "Software Engineer",
                "salary": 85000.00,
                "hire_date": date(2022, 1, 15),
                "status": "active",
                "address": "123 Main St, New York, NY 10001"
            },
            {
                "first_name": "Bob",
                "last_name": "Smith",
                "email": "bob.smith@example.com",
                "phone": "+1-555-0102",
                "department": "Sales",
                "position": "Sales Manager",
                "salary": 75000.00,
                "hire_date": date(2021, 6, 1),
                "status": "active",
                "address": "456 Oak Ave, Los Angeles, CA 90001"
            },
            {
                "first_name": "Carol",
                "last_name": "Williams",
                "email": "carol.williams@example.com",
                "phone": "+1-555-0103",
                "department": "Finance",
                "position": "Financial Analyst",
                "salary": 70000.00,
                "hire_date": date(2020, 3, 10),
                "status": "active",
                "address": "789 Pine Rd, Chicago, IL 60601"
            }
        ]
        
        for employee in sample_employees:
            self.create(employee)
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new employee record."""
        employee = {
            "id": self._next_id,
            **data,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        self._data[self._next_id] = employee
        self._next_id += 1
        logger.info(f"Created employee record with ID: {employee['id']}")
        return employee
    
    def get_by_id(self, item_id: int) -> Optional[Dict[str, Any]]:
        """Get an employee record by ID."""
        return self._data.get(item_id)
    
    def get_all(self, skip: int = 0, limit: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Get all employee records with pagination and optional filters."""
        employees = list(self._data.values())
        
        # Apply filters
        if filters:
            if "department" in filters:
                employees = [e for e in employees if e.get("department") == filters["department"]]
            if "status" in filters:
                employees = [e for e in employees if e.get("status") == filters["status"]]
            if "search" in filters:
                search_term = filters["search"].lower()
                employees = [
                    e for e in employees
                    if search_term in e.get("first_name", "").lower() or
                    search_term in e.get("last_name", "").lower() or
                    search_term in e.get("email", "").lower()
                ]
        
        # Apply pagination
        return employees[skip:skip + limit]
    
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count employee records with optional filters."""
        employees = list(self._data.values())
        
        if filters:
            if "department" in filters:
                employees = [e for e in employees if e.get("department") == filters["department"]]
            if "status" in filters:
                employees = [e for e in employees if e.get("status") == filters["status"]]
            if "search" in filters:
                search_term = filters["search"].lower()
                employees = [
                    e for e in employees
                    if search_term in e.get("first_name", "").lower() or
                    search_term in e.get("last_name", "").lower() or
                    search_term in e.get("email", "").lower()
                ]
        
        return len(employees)
    
    def update(self, item_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an employee record by ID."""
        if item_id not in self._data:
            return None
        
        # Update only provided fields
        for key, value in data.items():
            if value is not None:
                self._data[item_id][key] = value
        
        self._data[item_id]["updated_at"] = datetime.utcnow()
        logger.info(f"Updated employee record with ID: {item_id}")
        return self._data[item_id]
    
    def delete(self, item_id: int) -> bool:
        """Delete an employee record by ID."""
        if item_id in self._data:
            del self._data[item_id]
            logger.info(f"Deleted employee record with ID: {item_id}")
            return True
        return False


# Singleton instance
hr_repository = HRRepository()
