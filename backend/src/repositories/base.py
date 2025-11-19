"""
Base repository interface for data access layer.
"""
from typing import Generic, TypeVar, List, Optional, Dict, Any
from abc import ABC, abstractmethod

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """Abstract base repository with CRUD operations."""
    
    @abstractmethod
    def create(self, data: Dict[str, Any]) -> T:
        """Create a new record."""
        pass
    
    @abstractmethod
    def get_by_id(self, item_id: int) -> Optional[T]:
        """Get a record by ID."""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[T]:
        """Get all records with pagination and optional filters."""
        pass
    
    @abstractmethod
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count records with optional filters."""
        pass
    
    @abstractmethod
    def update(self, item_id: int, data: Dict[str, Any]) -> Optional[T]:
        """Update a record by ID."""
        pass
    
    @abstractmethod
    def delete(self, item_id: int) -> bool:
        """Delete a record by ID."""
        pass
