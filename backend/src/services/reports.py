"""
Service layer for Reports and analytics.
"""
from datetime import datetime
from ..repositories.inventory import inventory_repository
from ..repositories.sales import sales_repository
from ..repositories.purchases import purchases_repository
from ..repositories.hr import hr_repository
from ..repositories.accounting import accounting_repository
from ..schemas.reports import ReportSummary, SalesReportData, InventoryReportData, FinancialReportData
import logging

logger = logging.getLogger(__name__)


class ReportsService:
    """Service for generating reports and analytics."""
    
    def __init__(self):
        self.inventory_repo = inventory_repository
        self.sales_repo = sales_repository
        self.purchases_repo = purchases_repository
        self.hr_repo = hr_repository
        self.accounting_repo = accounting_repository
    
    def get_dashboard_summary(self) -> ReportSummary:
        """Generate dashboard summary report."""
        try:
            # Calculate total sales
            all_sales = self.sales_repo.get_all(skip=0, limit=10000)
            total_sales = sum(sale.get("total_amount", 0) for sale in all_sales)
            
            # Calculate total purchases
            all_purchases = self.purchases_repo.get_all(skip=0, limit=10000)
            total_purchases = sum(purchase.get("total_cost", 0) for purchase in all_purchases)
            
            # Calculate total inventory value
            all_inventory = self.inventory_repo.get_all(skip=0, limit=10000)
            total_inventory_value = sum(
                item.get("quantity", 0) * item.get("unit_price", 0)
                for item in all_inventory
            )
            
            # Count employees
            employee_count = self.hr_repo.count()
            
            # Count low stock items
            low_stock_items = sum(
                1 for item in all_inventory
                if item.get("quantity", 0) <= item.get("reorder_level", 0)
            )
            
            return ReportSummary(
                total_sales=total_sales,
                total_purchases=total_purchases,
                total_inventory_value=total_inventory_value,
                employee_count=employee_count,
                low_stock_items=low_stock_items,
                generated_at=datetime.utcnow()
            )
        except Exception as e:
            logger.error(f"Error generating dashboard summary: {str(e)}")
            raise
    
    def get_sales_report(self) -> SalesReportData:
        """Generate sales report."""
        try:
            all_sales = self.sales_repo.get_all(skip=0, limit=10000)
            
            total_sales = sum(sale.get("total_amount", 0) for sale in all_sales)
            total_transactions = len(all_sales)
            average_transaction = total_sales / total_transactions if total_transactions > 0 else 0
            
            # Calculate top items
            item_totals = {}
            for sale in all_sales:
                item_name = sale.get("item_name", "Unknown")
                amount = sale.get("total_amount", 0)
                item_totals[item_name] = item_totals.get(item_name, 0) + amount
            
            top_items = [
                {"item": item, "total": total}
                for item, total in sorted(item_totals.items(), key=lambda x: x[1], reverse=True)[:5]
            ]
            
            return SalesReportData(
                period="All Time",
                total_sales=total_sales,
                total_transactions=total_transactions,
                average_transaction=average_transaction,
                top_items=top_items
            )
        except Exception as e:
            logger.error(f"Error generating sales report: {str(e)}")
            raise
    
    def get_inventory_report(self) -> InventoryReportData:
        """Generate inventory report."""
        try:
            all_inventory = self.inventory_repo.get_all(skip=0, limit=10000)
            
            total_items = len(all_inventory)
            total_value = sum(
                item.get("quantity", 0) * item.get("unit_price", 0)
                for item in all_inventory
            )
            low_stock_count = sum(
                1 for item in all_inventory
                if item.get("quantity", 0) <= item.get("reorder_level", 0)
            )
            
            # Category breakdown
            category_totals = {}
            for item in all_inventory:
                category = item.get("category", "Unknown")
                value = item.get("quantity", 0) * item.get("unit_price", 0)
                if category not in category_totals:
                    category_totals[category] = {"items": 0, "value": 0}
                category_totals[category]["items"] += 1
                category_totals[category]["value"] += value
            
            categories = [
                {"category": cat, "items": data["items"], "value": data["value"]}
                for cat, data in category_totals.items()
            ]
            
            return InventoryReportData(
                total_items=total_items,
                total_value=total_value,
                low_stock_count=low_stock_count,
                categories=categories
            )
        except Exception as e:
            logger.error(f"Error generating inventory report: {str(e)}")
            raise
    
    def get_financial_report(self) -> FinancialReportData:
        """Generate financial report."""
        try:
            all_entries = self.accounting_repo.get_all(skip=0, limit=10000)
            
            total_revenue = sum(
                entry.get("amount", 0)
                for entry in all_entries
                if entry.get("transaction_type") == "credit"
            )
            total_expenses = sum(
                entry.get("amount", 0)
                for entry in all_entries
                if entry.get("transaction_type") == "debit"
            )
            net_profit = total_revenue - total_expenses
            profit_margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0
            
            return FinancialReportData(
                period="All Time",
                total_revenue=total_revenue,
                total_expenses=total_expenses,
                net_profit=net_profit,
                profit_margin=profit_margin
            )
        except Exception as e:
            logger.error(f"Error generating financial report: {str(e)}")
            raise


# Singleton instance
reports_service = ReportsService()
