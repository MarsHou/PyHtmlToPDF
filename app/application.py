"""
UtilityHub - Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.dependencies import check_and_install_dependencies
from app.api.v1.pdf import router as pdf_router
from app.api.v1.system import router as system_router

# Setup logging
logger = setup_logging()

# Initialize FastAPI app
app = FastAPI(
    title=settings.SERVICE_NAME,
    description=settings.SERVICE_DESCRIPTION,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(pdf_router, prefix="/api/v1")
app.include_router(system_router, prefix="/api/v1")

@app.get("/", summary="Root Endpoint")
async def root():
    """Root endpoint with service information"""
    return {
        "service": settings.SERVICE_NAME,
        "version": settings.VERSION,
        "description": settings.SERVICE_DESCRIPTION,
        "docs_url": "/docs",
        "api_prefix": "/api/v1"
    }

@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info(f"Starting {settings.SERVICE_NAME} v{settings.VERSION}")
    logger.info(f"API Documentation available at: /docs")
    logger.info(f"Service running on: {settings.HOST}:{settings.PORT}")

if __name__ == "__main__":
    # Check and install dependencies before starting
    check_and_install_dependencies()
    
    import uvicorn
    logger.info(f"Starting {settings.SERVICE_NAME} v{settings.VERSION}")
    uvicorn.run(
        "app.application:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )