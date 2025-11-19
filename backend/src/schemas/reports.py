"""
Pydantic schemas for Reports module.
"""
from typing import List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class ReportSummary(BaseModel):
    """Schema for report summary data."""
    total_sales: float = Field(..., description="Total sales amount")
    total_purchases: float = Field(..., description="Total purchases amount")
    total_inventory_value: float = Field(..., description="Total inventory value")
    employee_count: int = Field(..., description="Number of employees")
    low_stock_items: int = Field(..., description="Number of low stock items")
    generated_at: datetime = Field(..., description="Report generation timestamp")


class SalesReportData(BaseModel):
    """Schema for sales report data."""
    period: str = Field(..., description="Report period")
    total_sales: float = Field(..., description="Total sales")
    total_transactions: int = Field(..., description="Number of transactions")
    average_transaction: float = Field(..., description="Average transaction value")
    top_items: List[Dict[str, Any]] = Field(default=[], description="Top selling items")


class InventoryReportData(BaseModel):
    """Schema for inventory report data."""
    total_items: int = Field(..., description="Total number of items")
    total_value: float = Field(..., description="Total inventory value")
    low_stock_count: int = Field(..., description="Number of low stock items")
    categories: List[Dict[str, Any]] = Field(default=[], description="Category breakdown")


class FinancialReportData(BaseModel):
    """Schema for financial report data."""
    period: str = Field(..., description="Report period")
    total_revenue: float = Field(..., description="Total revenue")
    total_expenses: float = Field(..., description="Total expenses")
    net_profit: float = Field(..., description="Net profit")
    profit_margin: float = Field(..., description="Profit margin percentage")
