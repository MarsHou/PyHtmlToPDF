"""
Service registry for UtilityHub platform
"""

from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class ServiceInfo:
    """Service information model"""
    name: str
    description: str
    version: str
    endpoints: List[str]
    status: str = "active"
    dependencies: List[str] = None

class ServiceRegistry:
    """Registry for managing all services in UtilityHub"""
    
    def __init__(self):
        self._services: Dict[str, ServiceInfo] = {}
        self._initialize_core_services()
    
    def _initialize_core_services(self):
        """Initialize core services"""
        # PDF Service
        self.register_service(ServiceInfo(
            name="PDF Conversion",
            description="Convert URLs and HTML to PDF documents",
            version="1.0.0",
            endpoints=["/api/v1/pdf/url", "/api/v1/pdf/html"],
            dependencies=["playwright", "chromium"]
        ))
        
        # System Service
        self.register_service(ServiceInfo(
            name="System Management",
            description="Service health, logging, and system information",
            version="1.0.0",
            endpoints=["/api/v1/system/health", "/api/v1/system/info", "/api/v1/system/logs"]
        ))
    
    def register_service(self, service_info: ServiceInfo):
        """Register a new service"""
        self._services[service_info.name] = service_info
    
    def get_service(self, name: str) -> ServiceInfo:
        """Get service information by name"""
        return self._services.get(name)
    
    def list_services(self) -> List[ServiceInfo]:
        """List all registered services"""
        return list(self._services.values())
    
    def get_active_services(self) -> List[ServiceInfo]:
        """Get all active services"""
        return [service for service in self._services.values() if service.status == "active"]
    
    def get_service_endpoints(self) -> Dict[str, List[str]]:
        """Get all endpoints grouped by service"""
        return {name: service.endpoints for name, service in self._services.items()}
    
    def get_all_endpoints(self) -> List[str]:
        """Get all endpoints from all services"""
        endpoints = []
        for service in self._services.values():
            endpoints.extend(service.endpoints)
        return endpoints

# Global service registry instance
service_registry = ServiceRegistry()