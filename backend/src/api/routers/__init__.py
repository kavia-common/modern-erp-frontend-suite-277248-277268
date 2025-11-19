"""Routers module for API endpoints."""
from .health import router as health_router
from .inventory import router as inventory_router
from .sales import router as sales_router
from .purchases import router as purchases_router
from .accounting import router as accounting_router
from .hr import router as hr_router
from .reports import router as reports_router

__all__ = [
    "health_router",
    "inventory_router",
    "sales_router",
    "purchases_router",
    "accounting_router",
    "hr_router",
    "reports_router",
]
