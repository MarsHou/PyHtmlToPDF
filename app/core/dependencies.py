"""
Dependency management for UtilityHub service
"""

import logging
import subprocess
import sys
import importlib
import asyncio
from .config import settings

logger = logging.getLogger(__name__)

def check_package_installed(package_name: str) -> bool:
    """Check if a package is installed"""
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        return False

def install_package(package_name: str) -> bool:
    """Install a package using pip"""
    try:
        logger.info(f"Installing {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        logger.info(f"✓ Successfully installed {package_name}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"✗ Failed to install {package_name}: {e}")
        return False

def install_playwright_browsers() -> bool:
    """Install Playwright browsers"""
    try:
        logger.info("Installing Playwright browsers...")
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        logger.info("✓ Successfully installed Playwright browsers")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"✗ Failed to install Playwright browsers: {e}")
        return False

async def test_playwright_browser() -> bool:
    """Test if Playwright browser is available"""
    try:
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            await browser.close()
            return True
    except Exception:
        return False

def check_and_install_dependencies() -> bool:
    """Check and install all required dependencies"""
    logger.info("=== Starting Dependency Check ===")
    
    missing_packages = []
    for package in settings.REQUIRED_PACKAGES:
        if check_package_installed(package):
            logger.info(f"✓ {package} is already installed")
        else:
            missing_packages.append(package)
            logger.warning(f"✗ {package} is missing")
    
    if missing_packages:
        logger.warning(f"Missing packages: {missing_packages}")
        
        # Install from requirements.txt if available
        import os
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
        if asyncio.run(test_playwright_browser()):
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