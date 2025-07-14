# HTML to PDF Converter API

A Python FastAPI service that converts web pages or HTML source code to PDF files using Playwright.

## Features

- Convert web page URLs to PDF
- Convert HTML source code to PDF
- Customizable PDF options
- Async processing with proper error handling
- RESTful API with automatic documentation
- High-quality PDF generation with Playwright

## Installation

### Automatic Installation (Recommended)
The service will automatically check and install missing dependencies when started:

```bash
python main.py
```

The service will automatically:
- Check for required Python packages
- Install missing packages from requirements.txt
- Install Playwright browsers if needed
- Provide detailed logging of the installation process

### Manual Installation
If you prefer to install dependencies manually:

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install Playwright browsers:
```bash
playwright install chromium
```

## Usage

1. Start the server:
```bash
python main.py
```

2. The API will be available at `http://localhost:8000`

3. Access the interactive API documentation at `http://localhost:8000/docs`

## API Endpoints

### POST /convert/url
Convert a webpage URL to PDF

Headers:
- `x-request-id` (optional): Custom request ID for tracking

Request body:
```json
{
  "url": "https://example.com",
  "options": {
    "format": "A4",
    "margin": {
      "top": "0.75in",
      "right": "0.75in",
      "bottom": "0.75in",
      "left": "0.75in"
    }
  }
}
```

### POST /convert/html
Convert HTML source code to PDF

Headers:
- `x-request-id` (optional): Custom request ID for tracking

Request body:
```json
{
  "html": "<html><body><h1>Hello World</h1></body></html>",
  "options": {
    "format": "A4",
    "margin": {
      "top": "0.75in",
      "right": "0.75in",
      "bottom": "0.75in",
      "left": "0.75in"
    }
  }
}
```

### GET /logs
Get application logs

Query parameters:
- `limit` (optional, default: 100): Number of log entries to return
- `request_id` (optional): Filter logs by specific request ID

### GET /health
Health check endpoint - returns service status and version information

Response:
```json
{
  "status": "healthy",
  "service": "HTML to PDF Converter",
  "version": "1.2.0",
  "timestamp": "2024-07-14T10:30:00.123456",
  "build_date": "2024-07-14",
  "description": "HTML to PDF Converter with Playwright and Request Tracking"
}
```

## Configuration

Default PDF options:
- format: A4
- margin: 0.75in (all sides)
- print_background: true
- prefer_css_page_size: true

You can override these by passing custom options in the request body.

## Examples

### Convert URL to PDF
```bash
curl -X POST "http://localhost:8000/convert/url" \
  -H "Content-Type: application/json" \
  -H "x-request-id: my-custom-id-123" \
  -d '{"url": "https://www.google.com"}' \
  --output google.pdf
```

### Convert HTML to PDF
```bash
curl -X POST "http://localhost:8000/convert/html" \
  -H "Content-Type: application/json" \
  -H "x-request-id: my-custom-id-456" \
  -d '{"html": "<html><body><h1>Hello World</h1></body></html>"}' \
  --output hello.pdf
```

### Get Logs
```bash
# Get last 50 logs
curl "http://localhost:8000/logs?limit=50"

# Get logs for specific request ID
curl "http://localhost:8000/logs?request_id=my-custom-id-123"
```