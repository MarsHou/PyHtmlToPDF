"""
Core configuration for UtilityHub service
"""

import os
from typing import Dict, Any

class Settings:
    """Application settings"""
    
    # Service Information
    SERVICE_NAME = "UtilityHub"
    SERVICE_DESCRIPTION = "Multi-purpose utility service platform"
    VERSION = "1.0.0"
    
    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs.log")
    
    # PDF Service Configuration
    PDF_DEFAULT_FORMAT = "A4"
    PDF_DEFAULT_MARGIN = "1cm"
    
    # Service Dependencies
    REQUIRED_PACKAGES = [
        'fastapi',
        'uvicorn',
        'playwright',
        'pydantic'
    ]

settings = Settings()