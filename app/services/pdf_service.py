"""
PDF conversion service
"""

import io
import logging
import uuid
from typing import Dict, Any
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)

class PDFService:
    """PDF conversion service using Playwright"""
    
    def __init__(self):
        self.default_options = {
            'format': 'A4',
            'margin': {
                'top': '1cm',
                'right': '1cm',
                'bottom': '1cm',
                'left': '1cm'
            },
            'print_background': True,
            'prefer_css_page_size': True
        }
    
    async def convert_url_to_pdf(self, url: str, options: Dict[str, Any] = None, request_id: str = None) -> bytes:
        """Convert a URL to PDF"""
        request_id = request_id or str(uuid.uuid4())
        options = {**self.default_options, **(options or {})}
        
        logger.info(f"Request {request_id}: Starting URL to PDF conversion", extra={
            "request_id": request_id,
            "url": url,
            "options": options
        })
        
        try:
            async with async_playwright() as p:
                logger.info(f"Request {request_id}: Launching browser", extra={"request_id": request_id})
                browser = await p.chromium.launch()
                page = await browser.new_page()
                
                logger.info(f"Request {request_id}: Navigating to URL", extra={"request_id": request_id})
                await page.goto(url)
                await page.wait_for_load_state('networkidle')
                
                logger.info(f"Request {request_id}: Generating PDF", extra={"request_id": request_id})
                pdf_content = await page.pdf(**options)
                await browser.close()
            
            logger.info(f"Request {request_id}: PDF generation completed successfully", extra={
                "request_id": request_id,
                "pdf_size": len(pdf_content)
            })
            
            return pdf_content
            
        except Exception as e:
            logger.error(f"Request {request_id}: PDF conversion failed", extra={
                "request_id": request_id,
                "error": str(e),
                "url": url
            })
            raise
    
    async def convert_html_to_pdf(self, html: str, options: Dict[str, Any] = None, request_id: str = None) -> bytes:
        """Convert HTML content to PDF"""
        request_id = request_id or str(uuid.uuid4())
        options = {**self.default_options, **(options or {})}
        
        logger.info(f"Request {request_id}: Starting HTML to PDF conversion", extra={
            "request_id": request_id,
            "html_length": len(html),
            "options": options
        })
        
        try:
            async with async_playwright() as p:
                logger.info(f"Request {request_id}: Launching browser", extra={"request_id": request_id})
                browser = await p.chromium.launch()
                page = await browser.new_page()
                
                logger.info(f"Request {request_id}: Setting HTML content", extra={"request_id": request_id})
                await page.set_content(html)
                await page.wait_for_load_state('networkidle')
                
                logger.info(f"Request {request_id}: Generating PDF", extra={"request_id": request_id})
                pdf_content = await page.pdf(**options)
                await browser.close()
            
            logger.info(f"Request {request_id}: PDF generation completed successfully", extra={
                "request_id": request_id,
                "pdf_size": len(pdf_content)
            })
            
            return pdf_content
            
        except Exception as e:
            logger.error(f"Request {request_id}: PDF conversion failed", extra={
                "request_id": request_id,
                "error": str(e),
                "html_length": len(html)
            })
            raise