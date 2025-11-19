# ERP Backend API

A comprehensive FastAPI-based backend system providing REST APIs for Enterprise Resource Planning (ERP) operations including Inventory, Sales, Purchases, Accounting, HR, and Reports.

## 🚀 Features

- **RESTful API**: Clean, well-documented REST endpoints
- **OpenAPI/Swagger**: Auto-generated API documentation
- **CORS Support**: Configurable cross-origin resource sharing
- **Validation**: Comprehensive request/response validation using Pydantic
- **Pagination**: Efficient data pagination for large datasets
- **Error Handling**: Standardized error responses
- **Health Checks**: Built-in health check endpoints

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.100+
- **Python**: 3.9+
- **ASGI Server**: Uvicorn
- **Validation**: Pydantic v2
- **Data Storage**: In-memory (development)

## 📋 Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Virtual environment tool (venv recommended)

## 🔧 Environment Variables

Create a `.env` file in the `backend` directory with the following configuration:

```env
# Server Configuration
HOST=0.0.0.0
PORT=3001
UVICORN_HOST=0.0.0.0
UVICORN_WORKERS=1

# URLs
BACKEND_URL=http://localhost:3001
FRONTEND_URL=http://localhost:3000
SITE_URL=http://localhost:3000

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:4000
ALLOWED_HEADERS=Content-Type,Authorization,X-Requested-With
ALLOWED_METHODS=GET,POST,PUT,DELETE,PATCH,OPTIONS
CORS_MAX_AGE=3600

# Environment
NODE_ENV=development
TRUST_PROXY=true

# Security & Performance
REQUEST_TIMEOUT_MS=30000
RATE_LIMIT_WINDOW_S=60
RATE_LIMIT_MAX=100
```

### Environment Variable Descriptions

**Server Configuration:**
- `HOST`: Server bind address (0.0.0.0 for all interfaces)
- `PORT`: Server port number (default: 3001)
- `UVICORN_WORKERS`: Number of worker processes

**CORS Configuration:**
- `ALLOWED_ORIGINS`: Comma-separated list of allowed frontend URLs
  - **CRITICAL**: Must include your frontend URL (e.g., http://localhost:3000)
  - Add production URLs here when deploying
- `ALLOWED_HEADERS`: HTTP headers allowed in CORS requests
- `ALLOWED_METHODS`: HTTP methods allowed in CORS requests
- `CORS_MAX_AGE`: Preflight cache duration in seconds

**URLs:**
- `BACKEND_URL`: Backend API base URL
- `FRONTEND_URL`: Frontend application URL
- `SITE_URL`: Public site URL (used in emails, redirects)

## 📦 Installation

1. Navigate to the backend directory:
```bash
cd modern-erp-frontend-suite-277248-277268/backend
```

2. Create and activate a virtual environment:
```bash
# On Linux/Mac
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. Verify your `.env` file is configured correctly

## 🚀 Running the Application

### Development Mode

Start the server with auto-reload:

```bash
# Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 3001

# Or using Python module
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 3001
```

### Production Mode

Start the server for production:

```bash
# With multiple workers
uvicorn app.main:app --host 0.0.0.0 --port 3001 --workers 4

# Or with environment-based workers
uvicorn app.main:app --host 0.0.0.0 --port 3001 --workers $UVICORN_WORKERS
```

The API will be available at:
- **API Base**: http://localhost:3001
- **API Documentation**: http://localhost:3001/docs
- **OpenAPI Spec**: http://localhost:3001/openapi.json
- **ReDoc Documentation**: http://localhost:3001/redoc

## 📚 API Documentation

### Interactive Documentation

Visit `http://localhost:3001/docs` for interactive Swagger UI documentation where you can:
- Browse all available endpoints
- View request/response schemas
- Test API calls directly from the browser
- Download OpenAPI specification

### API Endpoints Overview

#### Health Check
- `GET /api/v1/` - Basic health check
- `GET /api/v1/health` - Detailed health status

#### Inventory Management
- `GET /api/v1/inventory/` - List inventory items (paginated)
- `POST /api/v1/inventory/` - Create inventory item
- `GET /api/v1/inventory/{item_id}` - Get specific item
- `PUT /api/v1/inventory/{item_id}` - Update item
- `DELETE /api/v1/inventory/{item_id}` - Delete item

#### Sales Management
- `GET /api/v1/sales/` - List sales (paginated)
- `POST /api/v1/sales/` - Create sale
- `GET /api/v1/sales/{sale_id}` - Get specific sale
- `PUT /api/v1/sales/{sale_id}` - Update sale
- `DELETE /api/v1/sales/{sale_id}` - Delete sale

#### Purchase Management
- `GET /api/v1/purchases/` - List purchases (paginated)
- `POST /api/v1/purchases/` - Create purchase
- `GET /api/v1/purchases/{purchase_id}` - Get specific purchase
- `PUT /api/v1/purchases/{purchase_id}` - Update purchase
- `DELETE /api/v1/purchases/{purchase_id}` - Delete purchase

#### Accounting
- `GET /api/v1/accounting/` - List accounting entries (paginated)
- `POST /api/v1/accounting/` - Create entry
- `GET /api/v1/accounting/{entry_id}` - Get specific entry
- `PUT /api/v1/accounting/{entry_id}` - Update entry
- `DELETE /api/v1/accounting/{entry_id}` - Delete entry

#### Human Resources
- `GET /api/v1/hr/employees` - List employees (paginated)
- `POST /api/v1/hr/employees` - Create employee
- `GET /api/v1/hr/employees/{employee_id}` - Get specific employee
- `PUT /api/v1/hr/employees/{employee_id}` - Update employee
- `DELETE /api/v1/hr/employees/{employee_id}` - Delete employee

#### Reports & Analytics
- `GET /api/v1/reports/summary` - Dashboard summary statistics
- `GET /api/v1/reports/sales` - Sales analytics
- `GET /api/v1/reports/inventory` - Inventory analytics
- `GET /api/v1/reports/financial` - Financial analytics

### Pagination

All list endpoints support pagination using query parameters:
- `skip` (integer): Number of records to skip (default: 0)
- `limit` (integer): Maximum records to return (default: 10, max: 100)

Example:
```
GET /api/v1/inventory?skip=20&limit=10
```

Response format:
```json
{
  "items": [...],
  "total": 100,
  "skip": 20,
  "limit": 10
}
```

### Filtering

Many endpoints support filtering via query parameters:

**Inventory:**
- `category`: Filter by category
- `search`: Search by name or SKU

**Sales:**
- `status`: Filter by status
- `customer_name`: Filter by customer

**Purchases:**
- `payment_status`: Filter by payment status
- `delivery_status`: Filter by delivery status
- `supplier_name`: Filter by supplier

**Accounting:**
- `transaction_type`: Filter by debit/credit
- `category`: Filter by category
- `account_name`: Filter by account

**HR:**
- `department`: Filter by department
- `status`: Filter by employment status
- `search`: Search by name or email

## 🔍 Testing the API

### Using curl

```bash
# Health check
curl http://localhost:3001/api/v1/health

# List inventory items
curl http://localhost:3001/api/v1/inventory?skip=0&limit=10

# Create inventory item
curl -X POST http://localhost:3001/api/v1/inventory \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "sku": "LAP-001",
    "category": "Electronics",
    "quantity": 50,
    "unit_price": 999.99
  }'
```

### Using Python requests

```python
import requests

# Get inventory
response = requests.get('http://localhost:3001/api/v1/inventory', params={'skip': 0, 'limit': 10})
data = response.json()
print(data)
```

## 🔐 CORS Configuration

### Understanding CORS

CORS (Cross-Origin Resource Sharing) allows the frontend (running on http://localhost:3000) to make requests to the backend (running on http://localhost:3001).

### Configuration

The backend CORS is configured via the `ALLOWED_ORIGINS` environment variable:

```env
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:4000
```

### Important Notes

1. **Multiple Origins**: Separate multiple URLs with commas (no spaces)
2. **Protocol Matters**: Use exact protocol (http:// or https://)
3. **Port Matters**: Include port numbers if not standard (80/443)
4. **No Trailing Slash**: URLs should not end with `/`

### Testing CORS

```bash
# Test preflight request
curl -X OPTIONS http://localhost:3001/api/v1/inventory \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: GET" \
  -v
```

Expected headers in response:
- `Access-Control-Allow-Origin: http://localhost:3000`
- `Access-Control-Allow-Methods: GET, POST, PUT, DELETE, PATCH, OPTIONS`
- `Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With`

## 🏗️ Project Structure

```
backend/
├── app/
│   ├── main.py              # Application entry point
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/   # API route handlers
│   │       │   ├── inventory.py
│   │       │   ├── sales.py
│   │       │   ├── purchases.py
│   │       │   ├── accounting.py
│   │       │   ├── hr.py
│   │       │   └── reports.py
│   │       └── router.py    # API router configuration
│   ├── models/              # Pydantic models/schemas
│   ├── services/            # Business logic layer
│   ├── core/                # Core configuration
│   │   ├── config.py        # Settings and environment
│   │   └── middleware.py    # CORS and middleware
│   └── utils/               # Utility functions
├── interfaces/
│   └── openapi.json         # OpenAPI specification
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## 🧪 Testing

Run tests (if available):
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=app --cov-report=html
```

## 🔍 Troubleshooting

### CORS Errors

**Problem**: Frontend shows "CORS policy blocked" errors

**Solutions**:
1. Verify `ALLOWED_ORIGINS` in `.env` includes frontend URL exactly
2. Restart backend server after changing `.env`
3. Check that frontend is using correct backend URL
4. Test CORS with curl (see Testing CORS section)

### Port Already in Use

**Problem**: `Address already in use` error

**Solutions**:
```bash
# Find process using port 3001
lsof -i :3001

# Kill the process
kill -9 <PID>

# Or use a different port
uvicorn app.main:app --reload --port 3002
```

### Module Import Errors

**Problem**: `ModuleNotFoundError` when starting server

**Solutions**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt

# Verify Python path
python -c "import sys; print(sys.path)"
```

### Environment Variables Not Loading

**Problem**: Server using default values instead of `.env`

**Solutions**:
1. Ensure `.env` file is in `backend/` directory
2. Install python-dotenv: `pip install python-dotenv`
3. Verify `.env` file has no syntax errors
4. Check file permissions: `chmod 644 .env`

### Validation Errors (422)

**Problem**: Getting 422 Unprocessable Entity errors

**Solutions**:
1. Check API documentation at `/docs` for required fields
2. Verify request body matches expected schema
3. Check data types (strings, integers, numbers)
4. View detailed error in response body

### Frontend Can't Connect

**Problem**: Frontend shows "Network Error" or "Backend unreachable"

**Checklist**:
1. Backend server is running: `curl http://localhost:3001/api/v1/health`
2. Backend port is 3001 (or matches `REACT_APP_BACKEND_URL`)
3. CORS is configured correctly
4. Firewall isn't blocking connections
5. Check backend console for errors

## 📊 Performance Tuning

### Production Deployment

```bash
# Use multiple workers (CPU cores * 2 + 1)
uvicorn app.main:app --host 0.0.0.0 --port 3001 --workers 4

# Behind a reverse proxy (nginx/traefik)
uvicorn app.main:app --host 127.0.0.1 --port 3001 --proxy-headers --forwarded-allow-ips='*'
```

### Optimization Tips

- Use connection pooling for database (when implemented)
- Enable HTTP caching headers for static responses
- Implement rate limiting for public APIs
- Use async operations for I/O-bound tasks
- Monitor with tools like Prometheus/Grafana

## 🔐 Security Best Practices

- Never commit `.env` files with secrets
- Use environment-specific `.env` files
- Implement authentication/authorization
- Enable HTTPS in production
- Set secure CORS policies (avoid `*`)
- Keep dependencies updated: `pip list --outdated`
- Use rate limiting in production
- Implement request validation
- Log security events
- Regular security audits

## 📝 Development Workflow

1. Activate virtual environment
2. Start backend server with `--reload`
3. Check API docs at http://localhost:3001/docs
4. Make code changes
5. Server auto-reloads on file changes
6. Test endpoints in Swagger UI
7. Check logs in terminal

## 🌐 Deployment

### Docker (recommended)

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3001"]
```

### Systemd Service

```ini
[Unit]
Description=ERP Backend API
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 3001
Restart=always

[Install]
WantedBy=multi-user.target
```

## 📞 Support

For issues or questions:
- Check API documentation at: http://localhost:3001/docs
- Review OpenAPI spec at: http://localhost:3001/openapi.json
- Check server logs in terminal
- Verify frontend README for integration details

## 📄 License

Proprietary - All rights reserved
