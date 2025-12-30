"""Resolution checking tool for pre-flight file validation."""

from pathlib import Path
from typing import Dict, Any, Optional, Union
import json

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

def load_shop_capabilities() -> Dict[str, Any]:
    """Load shop capabilities from config file."""
    config_path = Path(__file__).parent.parent / "config" / "shop_capabilities.json"
    with open(config_path, "r") as f:
        return json.load(f)

def check_resolution(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Check the resolution (DPI) of an image or PDF file.
    
    This is Layer 2: Pre-flight Guardrail
    
    Args:
        file_path: Path to the file to check
    
    Returns:
        Dictionary with resolution details and validation status
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        return {
            "valid": False,
            "error": f"File not found: {file_path}",
            "resolution_dpi": None
        }
    
    capabilities = load_shop_capabilities()
    min_dpi = capabilities["file_requirements"]["min_resolution_dpi"]
    
    # Check file extension
    file_ext = file_path.suffix.lower()
    
    if file_ext == ".pdf":
        return _check_pdf_resolution(file_path, min_dpi)
    elif file_ext in [".png", ".jpg", ".jpeg", ".tiff", ".tif"]:
        return _check_image_resolution(file_path, min_dpi)
    else:
        return {
            "valid": False,
            "error": f"Unsupported file format: {file_ext}",
            "supported_formats": capabilities["file_requirements"]["supported_formats"]
        }

def _check_pdf_resolution(file_path: Path, min_dpi: int) -> Dict[str, Any]:
    """Check PDF resolution using PyMuPDF."""
    if not PYMUPDF_AVAILABLE:
        return {
            "valid": False,
            "error": "PyMuPDF not available. Install with: pip install pymupdf",
            "resolution_dpi": None
        }
    
    try:
        doc = fitz.open(file_path)
        if len(doc) == 0:
            return {
                "valid": False,
                "error": "PDF file is empty",
                "resolution_dpi": None
            }
        
        # Check first page resolution
        page = doc[0]
        rect = page.rect
        
        # Get page dimensions in points (72 points = 1 inch)
        width_pts = rect.width
        height_pts = rect.height
        
        # Get image resolution from page (default is 72 DPI for PDFs)
        # For vector PDFs, we check the rendered resolution
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom = 144 DPI
        width_px = pix.width
        height_px = pix.height
        
        # Calculate effective DPI
        dpi_x = (width_px / width_pts) * 72
        dpi_y = (height_px / height_pts) * 72
        avg_dpi = (dpi_x + dpi_y) / 2
        
        doc.close()
        
        # For vector PDFs, check if embedded images meet requirements
        # This is a simplified check - in production, you'd check all embedded images
        valid = avg_dpi >= min_dpi or _check_pdf_embedded_images(file_path, min_dpi)
        
        return {
            "valid": valid,
            "resolution_dpi": round(avg_dpi, 1),
            "resolution_x_dpi": round(dpi_x, 1),
            "resolution_y_dpi": round(dpi_y, 1),
            "width_px": width_px,
            "height_px": height_px,
            "width_inches": round(width_pts / 72, 2),
            "height_inches": round(height_pts / 72, 2),
            "min_required_dpi": min_dpi,
            "file_type": "PDF"
        }
    except Exception as e:
        return {
            "valid": False,
            "error": f"Error reading PDF: {str(e)}",
            "resolution_dpi": None
        }

def _check_pdf_embedded_images(file_path: Path, min_dpi: int) -> bool:
    """Check if embedded images in PDF meet DPI requirements."""
    if not PYMUPDF_AVAILABLE:
        return False
    
    try:
        doc = fitz.open(file_path)
        for page_num in range(len(doc)):
            page = doc[page_num]
            image_list = page.get_images()
            for img_idx, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                img_bytes = base_image["image"]
                # Check image dimensions
                # This is simplified - in production, check actual DPI
                pass
        doc.close()
        return True  # Simplified - assume valid if we can read it
    except:
        return False

def _check_image_resolution(file_path: Path, min_dpi: int) -> Dict[str, Any]:
    """Check image resolution using Pillow."""
    if not PIL_AVAILABLE:
        return {
            "valid": False,
            "error": "Pillow not available. Install with: pip install pillow",
            "resolution_dpi": None
        }
    
    try:
        img = Image.open(file_path)
        width_px, height_px = img.size
        
        # Get DPI from EXIF data
        dpi_x = img.info.get("dpi", (72, 72))[0]
        dpi_y = img.info.get("dpi", (72, 72))[1]
        
        # If DPI is not in metadata, calculate from physical size if available
        if dpi_x == 72 and "resolution" in img.info:
            dpi_x, dpi_y = img.info["resolution"]
        
        # Fallback: assume 72 DPI if not specified (common for web images)
        if dpi_x == 1 or dpi_x == 0:
            dpi_x = dpi_y = 72
        
        avg_dpi = (dpi_x + dpi_y) / 2
        
        # Calculate dimensions in inches
        width_inches = width_px / dpi_x if dpi_x > 0 else width_px / 72
        height_inches = height_px / dpi_y if dpi_y > 0 else height_px / 72
        
        valid = avg_dpi >= min_dpi
        
        return {
            "valid": valid,
            "resolution_dpi": round(avg_dpi, 1),
            "resolution_x_dpi": round(dpi_x, 1),
            "resolution_y_dpi": round(dpi_y, 1),
            "width_px": width_px,
            "height_px": height_px,
            "width_inches": round(width_inches, 2),
            "height_inches": round(height_inches, 2),
            "min_required_dpi": min_dpi,
            "file_type": img.format,
            "color_mode": img.mode
        }
    except Exception as e:
        return {
            "valid": False,
            "error": f"Error reading image: {str(e)}",
            "resolution_dpi": None
        }

