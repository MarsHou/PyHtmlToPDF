#!/usr/bin/env python3
"""
UtilityHub - Entry point script
"""

import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.application import app
from app.core.dependencies import check_and_install_dependencies
from app.core.config import settings

if __name__ == "__main__":
    # Check and install dependencies before starting
    check_and_install_dependencies()
    
    import uvicorn
    print(f"🚀 Starting {settings.SERVICE_NAME} v{settings.VERSION}")
    print(f"📚 API Documentation: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"🔧 Service Features:")
    print(f"   • PDF Conversion (URL/HTML)")
    print(f"   • Request Tracking")
    print(f"   • System Monitoring")
    print(f"   • Automatic Dependencies")
    
    uvicorn.run(
        "app.application:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )