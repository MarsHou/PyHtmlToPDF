"""
System management API endpoints
"""

import os
import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

from app.core.config import settings
from app.core.service_registry import service_registry

router = APIRouter(prefix="/system", tags=["System Management"])
logger = logging.getLogger(__name__)

@router.get("/health", summary="Health Check")
async def health_check():
    """Health check endpoint with service information"""
    return {
        "status": "healthy",
        "service": settings.SERVICE_NAME,
        "version": settings.VERSION,
        "description": settings.SERVICE_DESCRIPTION,
        "timestamp": datetime.now().isoformat()
    }

@router.get("/info", summary="Service Information")
async def service_info():
    """Get detailed service information"""
    services = service_registry.get_active_services()
    
    return {
        "service": settings.SERVICE_NAME,
        "version": settings.VERSION,
        "description": settings.SERVICE_DESCRIPTION,
        "platform_features": [
            "Request Tracking",
            "Automatic Dependency Management", 
            "Structured Logging",
            "Modular Architecture",
            "Health Monitoring"
        ],
        "services": [
            {
                "name": service.name,
                "description": service.description,
                "version": service.version,
                "endpoints": service.endpoints,
                "status": service.status
            }
            for service in services
        ],
        "total_services": len(services),
        "all_endpoints": service_registry.get_all_endpoints()
    }

@router.get("/services", summary="List All Services")
async def list_services():
    """Get list of all registered services"""
    services = service_registry.list_services()
    
    return {
        "services": [
            {
                "name": service.name,
                "description": service.description,
                "version": service.version,
                "status": service.status,
                "endpoints": service.endpoints,
                "dependencies": service.dependencies or []
            }
            for service in services
        ],
        "total": len(services),
        "active": len(service_registry.get_active_services())
    }

@router.get("/logs", summary="Get Application Logs")
async def get_logs(limit: int = 100, request_id: str = None):
    """Get application logs with optional filtering"""
    try:
        logs = []
        log_file = settings.LOG_FILE
        
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