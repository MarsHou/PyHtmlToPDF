# UtilityHub - Project Structure Overview

## Project Transformation

This project has been transformed from a single-purpose HTML-to-PDF converter into a comprehensive **UtilityHub** - a modular utility service platform.

## New Architecture

### 🏗️ Modular Design
- **Service-Oriented**: Each utility is a separate service module
- **API Versioning**: Organized by API version (v1, v2, etc.)
- **Dependency Injection**: Core services are injectable and testable
- **Configuration Management**: Centralized configuration system

### 📁 Directory Structure

```
UtilityHub/
├── app/                           # Main application package
│   ├── __init__.py               # App-level version and info
│   ├── application.py            # FastAPI application setup
│   │
│   ├── core/                     # Core platform functionality
│   │   ├── config.py            # Settings and configuration
│   │   ├── dependencies.py      # Dependency management
│   │   ├── logging.py           # Logging configuration
│   │   └── service_registry.py  # Service discovery and registry
│   │
│   ├── models/                   # Data models and schemas
│   │   ├── __init__.py
│   │   └── pdf.py               # PDF service models
│   │
│   ├── services/                 # Business logic services
│   │   ├── __init__.py
│   │   └── pdf_service.py       # PDF conversion service
│   │
│   └── api/                      # API endpoints
│       └── v1/                   # API version 1
│           ├── __init__.py
│           ├── pdf.py           # PDF endpoints
│           └── system.py        # System management endpoints
│
├── main.py                      # Main entry point script
├── requirements.txt             # Python dependencies
├── README.md                    # Documentation
└── PROJECT_STRUCTURE.md         # Architecture overview (this file)
```

## Service Architecture

### 🔧 Core Services
1. **PDF Conversion Service** (`app/services/pdf_service.py`)
   - URL to PDF conversion
   - HTML to PDF conversion
   - Customizable options

2. **System Management Service** (`app/api/v1/system.py`)
   - Health monitoring
   - Service information
   - Log management
   - Service registry

### 🏗️ Application Structure
- **Entry Point** (`main.py`) - Project startup and configuration
- **Application Setup** (`app/application.py`) - FastAPI app configuration and middleware
- **Core Modules** (`app/core/`) - Platform-wide functionality
- **Service Modules** (`app/services/`) - Business logic implementations
- **API Modules** (`app/api/`) - REST endpoint definitions

### 🌐 API Structure
- **Base URL**: `http://localhost:8000`
- **API Prefix**: `/api/v1`
- **Documentation**: `/docs` (Swagger), `/redoc` (ReDoc)

### Current Endpoints:
```
GET  /                          # Root service info
GET  /api/v1/system/health      # Health check
GET  /api/v1/system/info        # Service information
GET  /api/v1/system/services    # List all services
GET  /api/v1/system/logs        # Get logs
POST /api/v1/pdf/url           # Convert URL to PDF
POST /api/v1/pdf/html          # Convert HTML to PDF
```

## Key Features

### 🚀 Platform Features
- **Auto-Dependency Management**: Automatic package and browser installation
- **Request Tracking**: UUID-based request correlation
- **Structured Logging**: JSON-formatted logs with correlation IDs
- **Service Registry**: Dynamic service discovery and management
- **Health Monitoring**: Comprehensive health checks
- **API Documentation**: Auto-generated OpenAPI/Swagger docs

### 🔄 Extensibility
The platform is designed for easy extension:

1. **Add New Service**:
   ```python
   # 1. Create model in app/models/
   # 2. Implement service in app/services/
   # 3. Add API endpoints in app/api/v1/
   # 4. Register in service registry
   ```

2. **Service Registry Integration**:
   ```python
   from app.core.service_registry import service_registry
   
   service_registry.register_service(ServiceInfo(
       name="New Service",
       description="Description",
       version="1.0.0",
       endpoints=["/api/v1/new/endpoint"]
   ))
   ```

## Migration Benefits

### From Single-Purpose to Platform
- ✅ **Scalability**: Easy to add new services
- ✅ **Maintainability**: Modular, organized codebase
- ✅ **Testability**: Separated concerns, injectable dependencies
- ✅ **Documentation**: Auto-generated API docs
- ✅ **Monitoring**: Built-in health checks and logging
- ✅ **Deployment**: Single entry point, auto-dependencies

### Clean Architecture
- All legacy files have been removed for a clean codebase
- Single entry point: `utility_hub.py`
- Modular, maintainable structure
- All original functionality preserved

## Usage

### Quick Start
```bash
# Single entry point
python main.py
```

### API Examples
```bash
# Service info
curl http://localhost:8000/api/v1/system/info

# List services
curl http://localhost:8000/api/v1/system/services

# Convert PDF (same as before)
curl -X POST "http://localhost:8000/api/v1/pdf/url" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

## Future Roadmap

### Planned Services
- **File Processing**: Image conversion, compression
- **Data Processing**: JSON/CSV/XML transformation
- **Text Processing**: Analysis, extraction, NLP
- **Notification Services**: Email, SMS, webhooks
- **Cache Services**: Redis utilities
- **Database Services**: Common DB operations

### Platform Enhancements
- **Authentication**: API key management
- **Rate Limiting**: Request throttling
- **Metrics**: Performance monitoring
- **Caching**: Response caching
- **Containerization**: Docker support

---

**UtilityHub** represents the evolution from a single-purpose tool to a comprehensive utility service platform, designed for scalability, maintainability, and extensibility.