"""Schemas module for Pydantic models."""
from .common import PaginationParams, PaginatedResponse, ErrorResponse, SuccessResponse
from .inventory import InventoryItemCreate, InventoryItemUpdate, InventoryItemResponse
from .sales import SaleCreate, SaleUpdate, SaleResponse
from .purchases import PurchaseCreate, PurchaseUpdate, PurchaseResponse
from .accounting import AccountingEntryCreate, AccountingEntryUpdate, AccountingEntryResponse
from .hr import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from .reports import ReportSummary, SalesReportData, InventoryReportData, FinancialReportData

__all__ = [
    "PaginationParams",
    "PaginatedResponse",
    "ErrorResponse",
    "SuccessResponse",
    "InventoryItemCreate",
    "InventoryItemUpdate",
    "InventoryItemResponse",
    "SaleCreate",
    "SaleUpdate",
    "SaleResponse",
    "PurchaseCreate",
    "PurchaseUpdate",
    "PurchaseResponse",
    "AccountingEntryCreate",
    "AccountingEntryUpdate",
    "AccountingEntryResponse",
    "EmployeeCreate",
    "EmployeeUpdate",
    "EmployeeResponse",
    "ReportSummary",
    "SalesReportData",
    "InventoryReportData",
    "FinancialReportData",
]
