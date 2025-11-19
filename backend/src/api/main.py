"""
Main FastAPI application for ERP Backend API.

This module initializes the FastAPI application with:
- CORS middleware configuration
- Router registration for all modules
- Global exception handlers
- API documentation setup
- Logging configuration
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
from ..core.config import settings
from .routers import (
    health_router,
    inventory_router,
    sales_router,
    purchases_router,
    accounting_router,
    hr_router,
    reports_router
)

# Configure logging
logger = logging.getLogger(__name__)

# API metadata for OpenAPI documentation
tags_metadata = [
    {
        "name": "Health",
        "description": "Health check endpoints for monitoring system status"
    },
    {
        "name": "Inventory",
        "description": "Operations for managing inventory items, stock levels, and product information"
    },
    {
        "name": "Sales",
        "description": "Operations for managing sales records, customer transactions, and order processing"
    },
    {
        "name": "Purchases",
        "description": "Operations for managing purchase orders, supplier transactions, and procurement"
    },
    {
        "name": "Accounting",
        "description": "Operations for managing accounting entries, transactions, and financial records"
    },
    {
        "name": "HR",
        "description": "Operations for managing employee records, departments, and human resources"
    },
    {
        "name": "Reports",
        "description": "Analytics and reporting endpoints for business intelligence and insights"
    }
]

# Initialize FastAPI application
app = FastAPI(
    title="ERP Backend API",
    description="""
    A comprehensive ERP (Enterprise Resource Planning) backend system providing REST APIs for:
    
    * **Inventory Management** - Track products, stock levels, and inventory movements
    * **Sales Management** - Process sales orders and customer transactions
    * **Purchase Management** - Handle purchase orders and supplier relationships
    * **Accounting** - Manage financial transactions and accounting entries
    * **Human Resources** - Maintain employee records and HR operations
    * **Reports & Analytics** - Generate business insights and analytics
    
    All endpoints follow RESTful conventions and include proper validation, error handling, and documentation.
    """,
    version="1.0.0",
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_origins_list(),
    allow_credentials=True,
    allow_methods=settings.get_methods_list(),
    allow_headers=settings.get_headers_list(),
    max_age=settings.cors_max_age
)


# Global exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Handle HTTP exceptions and return standardized error responses.
    
    Args:
        request: The incoming request
        exc: The HTTP exception
        
    Returns:
        JSONResponse: Standardized error response
    """
    logger.error(f"HTTP error occurred: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error_code": f"HTTP_{exc.status_code}"}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle request validation errors and return detailed error information.
    
    Args:
        request: The incoming request
        exc: The validation error
        
    Returns:
        JSONResponse: Detailed validation error response
    """
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "error_code": "VALIDATION_ERROR",
            "errors": exc.errors()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle unexpected exceptions and return generic error response.
    
    Args:
        request: The incoming request
        exc: The exception
        
    Returns:
        JSONResponse: Generic error response
    """
    logger.error(f"Unexpected error occurred: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred", "error_code": "INTERNAL_ERROR"}
    )


# Register routers
app.include_router(health_router, prefix="/api/v1")
app.include_router(inventory_router, prefix="/api/v1")
app.include_router(sales_router, prefix="/api/v1")
app.include_router(purchases_router, prefix="/api/v1")
app.include_router(accounting_router, prefix="/api/v1")
app.include_router(hr_router, prefix="/api/v1")
app.include_router(reports_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    """Execute tasks on application startup."""
    logger.info("ERP Backend API starting up...")
    logger.info(f"Environment: {settings.node_env}")
    logger.info(f"Allowed origins: {settings.get_origins_list()}")


@app.on_event("shutdown")
async def shutdown_event():
    """Execute tasks on application shutdown."""
    logger.info("ERP Backend API shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host=settings.uvicorn_host,
        port=settings.port,
        reload=True,
        log_level="info"
    )
