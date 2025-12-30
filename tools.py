"""
Agent Tools for Print Shop Order Processing
These tools are used by the ReAct agent to validate orders.
"""

import os
from PIL import Image
from pdf2image import convert_from_bytes
from pillow_heif import register_heif_opener
from shop_capabilities import SHOP_CAPABILITIES

register_heif_opener()

# Mock inventory database (in production, this would be a real database)
INVENTORY = {
    "80lb Glossy": {"available": True, "quantity": 500},
    "100lb Matte": {"available": True, "quantity": 300},
    "110lb Cardstock": {"available": True, "quantity": 200},
    "65lb Text": {"available": True, "quantity": 1000},
    "80lb Text": {"available": True, "quantity": 800},
}

# Mock pricing database
PRICING = {
    "base_price_per_sheet": 0.50,
    "size_multipliers": {
        "3x5": 0.5,
        "4x6": 0.6,
        "5x7": 0.7,
        "8x10": 1.0,
        "8.5x11": 1.2,
        "11x14": 1.8,
        "11x17": 2.5,
        "12x18": 3.0,
        "13x19": 3.5,
    },
    "paper_premiums": {
        "80lb Glossy": 0.10,
        "100lb Matte": 0.15,
        "110lb Cardstock": 0.25,
        "65lb Text": 0.0,
        "80lb Text": 0.05,
    },
    "quantity_discounts": {
        "1-10": 0.0,
        "11-50": 0.05,
        "51-100": 0.10,
        "101+": 0.15,
    }
}


def check_inventory(paper_type, quantity=1):
    """
    Tool: Check if paper stock is available in inventory.
    
    Args:
        paper_type: str - Paper type to check
        quantity: int - Quantity needed
    
    Returns:
        dict with availability status
    """
    paper_lower = paper_type.lower()
    
    # Find matching paper
    available_paper = None
    for paper in INVENTORY.keys():
        if paper.lower() in paper_lower or paper_lower in paper.lower():
            available_paper = paper
            break
    
    if not available_paper:
        return {
            "available": False,
            "message": f"Paper type '{paper_type}' not found in inventory.",
            "available_options": list(INVENTORY.keys())
        }
    
    stock = INVENTORY[available_paper]
    
    if not stock["available"]:
        return {
            "available": False,
            "message": f"Paper '{available_paper}' is currently out of stock.",
            "available_options": [p for p, v in INVENTORY.items() if v["available"]]
        }
    
    if stock["quantity"] < quantity:
        return {
            "available": False,
            "message": f"Only {stock['quantity']} sheets of '{available_paper}' available, but {quantity} requested.",
            "current_stock": stock["quantity"],
            "requested": quantity
        }
    
    return {
        "available": True,
        "paper": available_paper,
        "quantity_available": stock["quantity"],
        "message": f"Paper '{available_paper}' is available. Stock: {stock['quantity']} sheets."
    }


def check_resolution(file_path, target_width_inch, target_height_inch):
    """
    Tool: Check image resolution (DPI) for print quality.
    Layer 2: Pre-flight Guardrail
    
    Args:
        file_path: str - Path to image file
        target_width_inch: float - Target print width in inches
        target_height_inch: float - Target print height in inches
    
    Returns:
        dict with DPI analysis and quality status
    """
    try:
        # Handle different file types
        if file_path.lower().endswith('.pdf'):
            with open(file_path, 'rb') as f:
                images = convert_from_bytes(f.read())
                img = images[0] if images else None
        else:
            img = Image.open(file_path)
        
        if not img:
            return {
                "error": "Could not open image file.",
                "valid": False
            }
        
        width_px, height_px = img.size
        
        # Calculate DPI
        dpi_width = width_px / target_width_inch
        dpi_height = height_px / target_height_inch
        effective_dpi = min(dpi_width, dpi_height)  # Use worst case
        
        min_dpi = SHOP_CAPABILITIES["file_requirements"]["min_dpi"]
        recommended_dpi = SHOP_CAPABILITIES["file_requirements"]["recommended_dpi"]
        
        # Check quality
        if effective_dpi >= recommended_dpi:
            quality = "high"
            message = f"Excellent quality: {effective_dpi:.1f} DPI (Recommended: {recommended_dpi}+ DPI)"
        elif effective_dpi >= min_dpi:
            quality = "acceptable"
            message = f"Acceptable quality: {effective_dpi:.1f} DPI (Minimum: {min_dpi} DPI)"
        else:
            quality = "low"
            message = f"Low quality: {effective_dpi:.1f} DPI (Minimum required: {min_dpi} DPI). Image may appear pixelated."
        
        return {
            "valid": effective_dpi >= min_dpi,
            "quality": quality,
            "dpi": round(effective_dpi, 1),
            "dpi_width": round(dpi_width, 1),
            "dpi_height": round(dpi_height, 1),
            "pixel_dimensions": f"{width_px}x{height_px}",
            "target_size": f"{target_width_inch}\"x{target_height_inch}\"",
            "message": message,
            "meets_minimum": effective_dpi >= min_dpi,
            "meets_recommended": effective_dpi >= recommended_dpi
        }
    
    except Exception as e:
        return {
            "error": f"Error checking resolution: {str(e)}",
            "valid": False
        }


def calculate_price(size, paper_type, quantity=1):
    """
    Tool: Calculate price for print order.
    This is the ONLY source of truth for pricing.
    
    Args:
        size: str - Print size (e.g., "8x10")
        paper_type: str - Paper type
        quantity: int - Number of copies
    
    Returns:
        dict with price breakdown
    """
    # Get base price
    base_price = PRICING["base_price_per_sheet"]
    
    # Get size multiplier
    size_mult = PRICING["size_multipliers"].get(size, 1.0)
    
    # Get paper premium
    paper_premium = 0.0
    for paper, premium in PRICING["paper_premiums"].items():
        if paper.lower() in paper_type.lower():
            paper_premium = premium
            break
    
    # Calculate quantity discount
    discount_rate = 0.0
    if quantity >= 101:
        discount_rate = PRICING["quantity_discounts"]["101+"]
    elif quantity >= 51:
        discount_rate = PRICING["quantity_discounts"]["51-100"]
    elif quantity >= 11:
        discount_rate = PRICING["quantity_discounts"]["11-50"]
    
    # Calculate per-sheet price
    per_sheet = (base_price + paper_premium) * size_mult
    subtotal = per_sheet * quantity
    discount_amount = subtotal * discount_rate
    total = subtotal - discount_amount
    
    return {
        "base_price_per_sheet": base_price,
        "size_multiplier": size_mult,
        "paper_premium": paper_premium,
        "per_sheet_price": round(per_sheet, 2),
        "quantity": quantity,
        "subtotal": round(subtotal, 2),
        "discount_rate": discount_rate,
        "discount_amount": round(discount_amount, 2),
        "total": round(total, 2),
        "formatted_price": f"${total:.2f}"
    }

