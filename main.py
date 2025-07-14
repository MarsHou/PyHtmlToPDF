from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel, HttpUrl
import tempfile
import os
import io
from typing import Optional, List
import asyncio
import logging
import json
from datetime import datetime
import uuid
import subprocess
import sys
import importlib
from version import __version__, get_version_info

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Required dependencies
REQUIRED_PACKAGES = [
    'fastapi',
    'uvicorn',
    'playwright',
    'pydantic'
]

def check_package_installed(package_name):
    """Check if a package is installed"""
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        return False

def install_package(package_name):
    """Install a package using pip"""
    try:
        logger.info(f"Installing {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        logger.info(f"Successfully installed {package_name}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install {package_name}: {e}")
        return False

def install_playwright_browsers():
    """Install Playwright browsers"""
    try:
        logger.info("Installing Playwright browsers...")
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        logger.info("Successfully installed Playwright browsers")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install Playwright browsers: {e}")
        return False

def check_and_install_dependencies():
    """Check and install all required dependencies"""
    logger.info("=== Starting Dependency Check ===")
    
    missing_packages = []
    for package in REQUIRED_PACKAGES:
        if check_package_installed(package):
            logger.info(f"✓ {package} is already installed")
        else:
            missing_packages.append(package)
            logger.warning(f"✗ {package} is missing")
    
    if missing_packages:
        logger.warning(f"Missing packages: {missing_packages}")
        
        # Read and install from requirements.txt
        if os.path.exists('requirements.txt'):
            logger.info("Installing packages from requirements.txt...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
                logger.info("✓ Successfully installed packages from requirements.txt")
            except subprocess.CalledProcessError as e:
                logger.error(f"✗ Failed to install from requirements.txt: {e}")
                
                # Fallback: install individual packages
                for package in missing_packages:
                    install_package(package)
        else:
            # Install individual packages
            for package in missing_packages:
                install_package(package)
    else:
        logger.info("✓ All required packages are installed")
    
    # Check Playwright browsers
    logger.info("Checking Playwright browsers...")
    try:
        from playwright.async_api import async_playwright
        # Test if browsers are available
        import asyncio
        async def test_browser():
            async with async_playwright() as p:
                try:
                    browser = await p.chromium.launch()
                    await browser.close()
                    return True
                except Exception:
                    return False
        
        if asyncio.run(test_browser()):
            logger.info("✓ Playwright browsers are available")
        else:
            logger.warning("✗ Playwright browsers not available, installing...")
            install_playwright_browsers()
            
    except Exception as e:
        logger.warning(f"Could not test Playwright browsers: {e}")
        logger.info("Installing Playwright browsers as fallback...")
        install_playwright_browsers()
    
    logger.info("=== Dependency Check Completed ===")
    return True

# Now import playwright after ensuring it's installed
try:
    from playwright.async_api import async_playwright
except ImportError:
    logger.error("Playwright import failed even after installation attempt")
    sys.exit(1)

app = FastAPI(title="HTML to PDF Converter", version=__version__)

class URLRequest(BaseModel):
    url: HttpUrl
    options: Optional[dict] = None

class HTMLRequest(BaseModel):
    html: str
    options: Optional[dict] = None

class LogEntry(BaseModel):
    timestamp: str
    request_id: str
    level: str
    message: str
    details: Optional[dict] = None

# Default PDF options for Playwright
DEFAULT_OPTIONS = {
    'format': 'A4',
    'margin': {
        'top': '0.75in',
        'right': '0.75in',
        'bottom': '0.75in',
        'left': '0.75in'
    },
    'print_background': True,
    'prefer_css_page_size': True
}

@app.get("/")
async def root():
    return {
        "message": "HTML to PDF Converter API",
        "version": __version__,
        **get_version_info()
    }

@app.post("/convert/url")
async def convert_url_to_pdf(request: URLRequest, req: Request, x_request_id: str = Header(None)):
    """Convert webpage URL to PDF"""
    request_id = x_request_id or str(uuid.uuid4())
    
    logger.info(f"Request {request_id}: Starting URL to PDF conversion", extra={
        "request_id": request_id,
        "url": str(request.url),
        "options": request.options
    })
    
    try:
        # Merge custom options with defaults
        options = {**DEFAULT_OPTIONS, **(request.options or {})}
        
        logger.info(f"Request {request_id}: Launching browser", extra={"request_id": request_id})
        
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            
            logger.info(f"Request {request_id}: Navigating to URL", extra={"request_id": request_id})
            await page.goto(str(request.url))
            await page.wait_for_load_state('networkidle')
            
            logger.info(f"Request {request_id}: Generating PDF", extra={"request_id": request_id})
            pdf_content = await page.pdf(**options)
            await browser.close()
        
        logger.info(f"Request {request_id}: PDF generation completed successfully", extra={
            "request_id": request_id,
            "pdf_size": len(pdf_content)
        })
        
        return StreamingResponse(
            io.BytesIO(pdf_content),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=webpage.pdf"}
        )
        
    except Exception as e:
        logger.error(f"Request {request_id}: PDF conversion failed", extra={
            "request_id": request_id,
            "error": str(e),
            "url": str(request.url)
        })
        raise HTTPException(status_code=500, detail=f"PDF conversion failed: {str(e)}")

@app.post("/convert/html")
async def convert_html_to_pdf(request: HTMLRequest, req: Request, x_request_id: str = Header(None)):
    """Convert HTML source code to PDF"""
    request_id = x_request_id or str(uuid.uuid4())
    
    logger.info(f"Request {request_id}: Starting HTML to PDF conversion", extra={
        "request_id": request_id,
        "html_length": len(request.html),
        "options": request.options
    })
    
    try:
        # Merge custom options with defaults
        options = {**DEFAULT_OPTIONS, **(request.options or {})}
        
        logger.info(f"Request {request_id}: Launching browser", extra={"request_id": request_id})
        
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            
            logger.info(f"Request {request_id}: Setting HTML content", extra={"request_id": request_id})
            await page.set_content(request.html)
            await page.wait_for_load_state('networkidle')
            
            logger.info(f"Request {request_id}: Generating PDF", extra={"request_id": request_id})
            pdf_content = await page.pdf(**options)
            await browser.close()
        
        logger.info(f"Request {request_id}: PDF generation completed successfully", extra={
            "request_id": request_id,
            "pdf_size": len(pdf_content)
        })
        
        return StreamingResponse(
            io.BytesIO(pdf_content),
            media_type="application/pdf", 
            headers={"Content-Disposition": "attachment; filename=document.pdf"}
        )
        
    except Exception as e:
        logger.error(f"Request {request_id}: PDF conversion failed", extra={
            "request_id": request_id,
            "error": str(e),
            "html_length": len(request.html)
        })
        raise HTTPException(status_code=500, detail=f"PDF conversion failed: {str(e)}")

@app.get("/logs")
async def get_logs(limit: int = 100, request_id: str = None):
    """Get application logs"""
    try:
        logs = []
        log_file = "app.log"
        
        if not os.path.exists(log_file):
            return {"logs": [], "message": "No log file found"}
        
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Filter by request_id if provided
        if request_id:
            lines = [line for line in lines if request_id in line]
        
        # Get the last 'limit' lines
        lines = lines[-limit:]
        
        for line in lines:
            line = line.strip()
            if line:
                logs.append({
                    "timestamp": datetime.now().isoformat(),
                    "raw_log": line
                })
        
        return {
            "logs": logs,
            "total": len(logs),
            "limit": limit,
            "request_id_filter": request_id
        }
        
    except Exception as e:
        logger.error(f"Failed to read logs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read logs: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "HTML to PDF Converter",
        "version": __version__,
        "timestamp": datetime.now().isoformat(),
        **get_version_info()
    }

if __name__ == "__main__":
    # Check and install dependencies before starting the server
    check_and_install_dependencies()
    
    import uvicorn
    logger.info(f"Starting HTML to PDF Converter v{__version__}")
    uvicorn.run(app, host="0.0.0.0", port=8000)