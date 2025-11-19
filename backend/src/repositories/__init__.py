"""Repositories module for data access layer."""
from .inventory import inventory_repository
from .sales import sales_repository
from .purchases import purchases_repository
from .accounting import accounting_repository
from .hr import hr_repository

__all__ = [
    "inventory_repository",
    "sales_repository",
    "purchases_repository",
    "accounting_repository",
    "hr_repository",
]
