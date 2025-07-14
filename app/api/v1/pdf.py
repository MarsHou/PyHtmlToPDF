"""
PDF conversion API endpoints
"""

import io
import uuid
from fastapi import APIRouter, HTTPException, Request, Header
from fastapi.responses import StreamingResponse

from app.models.pdf import URLToPDFRequest, HTMLToPDFRequest
from app.services.pdf_service import PDFService

router = APIRouter(prefix="/pdf", tags=["PDF Conversion"])
pdf_service = PDFService()

@router.post("/url", summary="Convert URL to PDF")
async def convert_url_to_pdf(
    request: URLToPDFRequest, 
    req: Request, 
    x_request_id: str = Header(None)
):
    """Convert a webpage URL to PDF"""
    request_id = x_request_id or str(uuid.uuid4())
    
    try:
        pdf_content = await pdf_service.convert_url_to_pdf(
            url=str(request.url),
            options=request.options,
            request_id=request_id
        )
        
        return StreamingResponse(
            io.BytesIO(pdf_content),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=webpage.pdf"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF conversion failed: {str(e)}")

@router.post("/html", summary="Convert HTML to PDF")
async def convert_html_to_pdf(
    request: HTMLToPDFRequest, 
    req: Request, 
    x_request_id: str = Header(None)
):
    """Convert HTML source code to PDF"""
    request_id = x_request_id or str(uuid.uuid4())
    
    try:
        pdf_content = await pdf_service.convert_html_to_pdf(
            html=request.html,
            options=request.options,
            request_id=request_id
        )
        
        return StreamingResponse(
            io.BytesIO(pdf_content),
            media_type="application/pdf", 
            headers={"Content-Disposition": "attachment; filename=document.pdf"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF conversion failed: {str(e)}")