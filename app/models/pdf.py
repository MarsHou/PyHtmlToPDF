"""
Data models for PDF service
"""

from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, Any

class PDFRequest(BaseModel):
    """Base PDF request model"""
    options: Optional[Dict[str, Any]] = None

class URLToPDFRequest(PDFRequest):
    """Request model for URL to PDF conversion"""
    url: HttpUrl

class HTMLToPDFRequest(PDFRequest):
    """Request model for HTML to PDF conversion"""
    html: str

class LogEntry(BaseModel):
    """Log entry model"""
    timestamp: str
    request_id: str
    level: str
    message: str
    details: Optional[Dict[str, Any]] = None