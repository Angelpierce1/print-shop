"""Inventory checking tool for validating order specifications."""

import json
from pathlib import Path
from typing import Dict, Any, Optional

def load_shop_capabilities() -> Dict[str, Any]:
    """Load shop capabilities from config file."""
    config_path = Path(__file__).parent.parent / "config" / "shop_capabilities.json"
    with open(config_path, "r") as f:
        return json.load(f)

def check_inventory(paper_stock: str, color: str, finish: str) -> Dict[str, Any]:
    """
    Check if a paper stock combination is available.
    
    Args:
        paper_stock: Paper stock type (e.g., "100lb_cardstock")
        color: Paper color (e.g., "white", "black")
        finish: Paper finish (e.g., "matte", "gloss")
    
    Returns:
        Dictionary with availability status and details
    """
    capabilities = load_shop_capabilities()
    
    # Check if paper stock exists
    if paper_stock not in capabilities["paper_stocks"]:
        return {
            "available": False,
            "reason": f"Paper stock '{paper_stock}' is not available in our inventory.",
            "available_stocks": list(capabilities["paper_stocks"].keys())
        }
    
    stock_info = capabilities["paper_stocks"][paper_stock]
    
    # Check if stock is available
    if not stock_info["available"]:
        return {
            "available": False,
            "reason": f"Paper stock '{paper_stock}' is currently out of stock."
        }
    
    # Check if color is available for this stock
    if color not in stock_info["colors"]:
        return {
            "available": False,
            "reason": f"Color '{color}' is not available for '{paper_stock}'.",
            "available_colors": stock_info["colors"],
            "white_ink_capable": stock_info["white_ink_capable"]
        }
    
    # Check if finish is available
    if finish not in stock_info["finish"]:
        return {
            "available": False,
            "reason": f"Finish '{finish}' is not available for '{paper_stock}'.",
            "available_finishes": stock_info["finish"]
        }
    
    return {
        "available": True,
        "paper_stock": paper_stock,
        "color": color,
        "finish": finish,
        "white_ink_capable": stock_info["white_ink_capable"]
    }




