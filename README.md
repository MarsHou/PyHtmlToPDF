# UtilityHub - Multi-Purpose Utility Service Platform

UtilityHub is a comprehensive, modular utility service platform designed to provide various API services for common development and business needs. Currently featuring PDF conversion capabilities with plans for additional utility services.

## 🚀 Features

### Current Services
- **PDF Conversion Service**
  - Convert web page URLs to PDF
  - Convert HTML source code to PDF
  - Customizable PDF options (format, margins, etc.)
  - High-quality generation with Playwright

### Platform Features
- **Request Tracking**: Full request lifecycle logging with custom request IDs
- **Automatic Dependencies**: Self-installing required packages and browsers
- **Structured Logging**: Comprehensive logging with request correlation
- **Health Monitoring**: Service health and status endpoints
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Modular Architecture**: Easy to extend with new services

## 📁 Project Structure

```
UtilityHub/
├── app/                        # Main application package
│   ├── __init__.py            # App version and metadata
│   ├── application.py         # FastAPI application setup
│   ├── core/                  # Core functionality
│   │   ├── config.py          # Configuration management
│   │   ├── dependencies.py    # Dependency management
│   │   ├── logging.py         # Logging configuration
│   │   └── service_registry.py # Service discovery
│   ├── models/                # Data models
│   │   ├── __init__.py
│   │   └── pdf.py             # PDF service models
│   ├── services/              # Service implementations
│   │   ├── __init__.py
│   │   └── pdf_service.py     # PDF conversion service
│   └── api/                   # API endpoints
│       └── v1/                # API version 1
│           ├── __init__.py
│           ├── pdf.py         # PDF endpoints
│           └── system.py      # System endpoints
├── main.py                    # Main entry point
├── requirements.txt           # Python dependencies
├── README.md                  # Documentation
└── PROJECT_STRUCTURE.md       # Architecture overview
```

## 🛠 Installation & Setup

### Quick Start (Recommended)
Simply run the service - it will automatically install all dependencies:

```bash
python main.py
```

The service will automatically:
- ✅ Check for required Python packages
- 📦 Install missing packages from requirements.txt
- 🌐 Install Playwright browsers if needed
- 📝 Provide detailed logging of the installation process
- 🚀 Start the service

### Manual Installation
If you prefer manual setup:

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Start the service
python main.py
```

## 🔗 API Usage

### Service Information
```bash
# Service root
curl http://localhost:8000/

# Health check
curl http://localhost:8000/api/v1/system/health

# Service information
curl http://localhost:8000/api/v1/system/info
```

### PDF Conversion Service

#### Convert URL to PDF
```bash
curl -X POST \"http://localhost:8000/api/v1/pdf/url\" \\
  -H \"Content-Type: application/json\" \\
  -H \"x-request-id: my-request-123\" \\
  -d '{\"url\": \"https://www.google.com\"}' \\
  --output webpage.pdf
```

#### Convert HTML to PDF
```bash
curl -X POST \"http://localhost:8000/api/v1/pdf/html\" \\
  -H \"Content-Type: application/json\" \\
  -H \"x-request-id: my-request-456\" \\
  -d '{\"html\": \"<html><body><h1>Hello World</h1></body></html>\"}' \\
  --output document.pdf
```

#### Custom PDF Options
```bash
curl -X POST \"http://localhost:8000/api/v1/pdf/url\" \\
  -H \"Content-Type: application/json\" \\
  -d '{
    \"url\": \"https://example.com\",
    \"options\": {
      \"format\": \"A4\",
      \"margin\": {
        \"top\": \"2cm\",
        \"right\": \"2cm\",
        \"bottom\": \"2cm\",
        \"left\": \"2cm\"
      },
      \"print_background\": true
    }
  }' \\
  --output custom.pdf
```

### System Management

#### Get Logs
```bash
# Get recent logs
curl \"http://localhost:8000/api/v1/system/logs?limit=50\"

# Get logs for specific request
curl \"http://localhost:8000/api/v1/system/logs?request_id=my-request-123\"
```

## 📚 API Documentation

Once the service is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Configuration

The service can be configured via environment variables:

```bash
# Server Configuration
export HOST=0.0.0.0
export PORT=8000
export DEBUG=false

# Logging Configuration
export LOG_LEVEL=INFO
export LOG_FILE=utility_hub.log
```

## 🎯 Extending the Platform

UtilityHub is designed for easy extension. To add a new service:

1. **Create Service Model** in `app/models/`
2. **Implement Service Logic** in `app/services/`
3. **Add API Endpoints** in `app/api/v1/`
4. **Register Router** in `app/main.py`

### Example: Adding a new service
```python
# app/services/new_service.py
class NewService:
    async def process_data(self, data: str) -> str:
        # Service implementation
        return processed_data

# app/api/v1/new_endpoints.py
from fastapi import APIRouter
router = APIRouter(prefix=\"/new\", tags=[\"New Service\"])

@router.post(\"/process\")
async def process_endpoint(data: str):
    service = NewService()
    result = await service.process_data(data)
    return {\"result\": result}
```

## 🔍 Monitoring & Logging

- **Request Tracking**: Every request gets a unique ID for full traceability
- **Structured Logs**: JSON-formatted logs with correlation IDs
- **Health Endpoints**: Monitor service status and dependencies
- **Performance Metrics**: Request timing and success rates

## 🚀 Future Services (Roadmap)

- **File Processing**: Image conversion, compression, format transformation
- **Data Processing**: JSON/CSV/XML processing and transformation
- **Text Processing**: Text analysis, extraction, and transformation
- **Notification Services**: Email, SMS, webhook notifications
- **Cache Services**: Redis-based caching utilities
- **Database Services**: Common database operations and utilities

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

---

**UtilityHub** - Your one-stop utility service platform for development and business needs.