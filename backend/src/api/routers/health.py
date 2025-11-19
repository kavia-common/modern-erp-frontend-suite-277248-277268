"""
Health check router for monitoring system status.
"""
from fastapi import APIRouter, status
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Health"])


# PUBLIC_INTERFACE
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Check if the API is running and responsive"
)
async def health_check():
    """
    Health check endpoint to verify API availability.
    
    Returns:
        dict: Status message and timestamp
    """
    return {
        "status": "healthy",
        "message": "ERP Backend API is running",
        "timestamp": datetime.utcnow().isoformat()
    }


# PUBLIC_INTERFACE
@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Detailed Health Check",
    description="Get detailed health status of the API and its components"
)
async def detailed_health():
    """
    Detailed health check with component status.
    
    Returns:
        dict: Detailed health information
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "api": "operational",
            "repositories": "operational"
        }
    }
