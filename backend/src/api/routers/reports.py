"""
Reports router for generating analytics and reports.
"""
from fastapi import APIRouter, HTTPException, status
from ...schemas.reports import ReportSummary, SalesReportData, InventoryReportData, FinancialReportData
from ...services.reports import reports_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reports", tags=["Reports"])


# PUBLIC_INTERFACE
@router.get(
    "/summary",
    response_model=ReportSummary,
    summary="Dashboard Summary",
    description="Get summary statistics for the dashboard"
)
async def get_dashboard_summary():
    """
    Get dashboard summary with key metrics.
    
    Returns:
        ReportSummary: Dashboard summary data
    """
    try:
        return reports_service.get_dashboard_summary()
    except Exception as e:
        logger.error(f"Error generating dashboard summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate dashboard summary"
        )


# PUBLIC_INTERFACE
@router.get(
    "/sales",
    response_model=SalesReportData,
    summary="Sales Report",
    description="Get detailed sales analytics and statistics"
)
async def get_sales_report():
    """
    Get sales report with analytics.
    
    Returns:
        SalesReportData: Sales report data
    """
    try:
        return reports_service.get_sales_report()
    except Exception as e:
        logger.error(f"Error generating sales report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate sales report"
        )


# PUBLIC_INTERFACE
@router.get(
    "/inventory",
    response_model=InventoryReportData,
    summary="Inventory Report",
    description="Get inventory analytics and statistics"
)
async def get_inventory_report():
    """
    Get inventory report with analytics.
    
    Returns:
        InventoryReportData: Inventory report data
    """
    try:
        return reports_service.get_inventory_report()
    except Exception as e:
        logger.error(f"Error generating inventory report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate inventory report"
        )


# PUBLIC_INTERFACE
@router.get(
    "/financial",
    response_model=FinancialReportData,
    summary="Financial Report",
    description="Get financial analytics including revenue, expenses, and profit"
)
async def get_financial_report():
    """
    Get financial report with analytics.
    
    Returns:
        FinancialReportData: Financial report data
    """
    try:
        return reports_service.get_financial_report()
    except Exception as e:
        logger.error(f"Error generating financial report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate financial report"
        )
