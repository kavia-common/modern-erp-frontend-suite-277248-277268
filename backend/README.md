# ERP Backend API

A comprehensive FastAPI-based backend system for Enterprise Resource Planning (ERP) operations.

## Features

- **Inventory Management** - CRUD operations for inventory items with filtering and pagination
- **Sales Management** - Track sales records and customer transactions
- **Purchase Management** - Handle purchase orders and supplier relationships
- **Accounting** - Manage financial transactions and accounting entries
- **HR Management** - Employee records and human resources operations
- **Reports & Analytics** - Generate business insights and analytics

## Architecture

The backend follows a clean, layered architecture:

```
backend/
├── src/
│   ├── api/
│   │   ├── main.py           # FastAPI application entry point
│   │   └── routers/          # API route handlers
│   ├── core/
│   │   └── config.py         # Application configuration
│   ├── schemas/              # Pydantic models for validation
│   ├── services/             # Business logic layer
│   └── repositories/         # Data access layer (in-memory stores)
├── tests/                    # Test suite
└── requirements.txt          # Python dependencies
```

## Technology Stack

- **FastAPI** - Modern, high-performance web framework
- **Pydantic** - Data validation using Python type hints
- **Uvicorn** - ASGI server for production deployment
- **Pytest** - Testing framework

## Setup

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Installation

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Environment variables are configured in `.env` file (already present)

3. Run the development server:
```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload
```

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:3001/docs
- **ReDoc**: http://localhost:3001/redoc
- **OpenAPI JSON**: http://localhost:3001/openapi.json

## API Endpoints

### Health
- `GET /api/v1/` - Basic health check
- `GET /api/v1/health` - Detailed health check

### Inventory
- `GET /api/v1/inventory/` - List inventory items (with pagination & filters)
- `GET /api/v1/inventory/{id}` - Get inventory item by ID
- `POST /api/v1/inventory/` - Create new inventory item
- `PUT /api/v1/inventory/{id}` - Update inventory item
- `DELETE /api/v1/inventory/{id}` - Delete inventory item

### Sales
- `GET /api/v1/sales/` - List sales records
- `GET /api/v1/sales/{id}` - Get sale by ID
- `POST /api/v1/sales/` - Create new sale
- `PUT /api/v1/sales/{id}` - Update sale
- `DELETE /api/v1/sales/{id}` - Delete sale

### Purchases
- `GET /api/v1/purchases/` - List purchase records
- `GET /api/v1/purchases/{id}` - Get purchase by ID
- `POST /api/v1/purchases/` - Create new purchase
- `PUT /api/v1/purchases/{id}` - Update purchase
- `DELETE /api/v1/purchases/{id}` - Delete purchase

### Accounting
- `GET /api/v1/accounting/` - List accounting entries
- `GET /api/v1/accounting/{id}` - Get entry by ID
- `POST /api/v1/accounting/` - Create new entry
- `PUT /api/v1/accounting/{id}` - Update entry
- `DELETE /api/v1/accounting/{id}` - Delete entry

### HR
- `GET /api/v1/hr/employees` - List employees
- `GET /api/v1/hr/employees/{id}` - Get employee by ID
- `POST /api/v1/hr/employees` - Create new employee
- `PUT /api/v1/hr/employees/{id}` - Update employee
- `DELETE /api/v1/hr/employees/{id}` - Delete employee

### Reports
- `GET /api/v1/reports/summary` - Dashboard summary
- `GET /api/v1/reports/sales` - Sales report
- `GET /api/v1/reports/inventory` - Inventory report
- `GET /api/v1/reports/financial` - Financial report

## Testing

Run the test suite:

```bash
pytest tests/ -v
```

Run tests with coverage:

```bash
pytest tests/ --cov=src --cov-report=html
```

## Data Storage

Currently using in-memory data stores with sample data. In production, these would be replaced with actual database connections (PostgreSQL, MongoDB, etc.).

## Security Features

- CORS configuration for cross-origin requests
- Request validation using Pydantic schemas
- Proper error handling and logging
- No hardcoded secrets (uses environment variables)

## Development

The API follows these best practices:

- **Layered Architecture** - Separation of concerns (routers → services → repositories)
- **Type Hints** - Full type annotations throughout
- **Documentation** - Comprehensive docstrings and OpenAPI specs
- **Error Handling** - Proper exception handling and user-friendly error messages
- **Logging** - Structured logging for debugging and monitoring
- **Testing** - Unit and integration tests

## Production Deployment

For production deployment:

1. Set `NODE_ENV=production` in environment variables
2. Configure proper CORS origins
3. Use production-grade database instead of in-memory stores
4. Enable HTTPS/TLS
5. Configure proper logging and monitoring
6. Use multiple Uvicorn workers: `uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --workers 4`

## License

MIT License
