"""Pricing calculation tool - must be used for all price quotes."""

import json
from pathlib import Path
from typing import Dict, Any, Optional

def load_pricing_config() -> Dict[str, Any]:
    """Load pricing configuration from config file."""
    config_path = Path(__file__).parent.parent / "config" / "pricing.json"
    with open(config_path, "r") as f:
        return json.load(f)

def calculate_price(
    paper_stock: str,
    quantity: int,
    width_inches: float,
    height_inches: float,
    full_color: bool = True,
    rush_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Calculate the price for a print order.
    
    This tool MUST be used for all price calculations.
    The agent must never estimate prices without using this tool.
    
    Args:
        paper_stock: Paper stock type (e.g., "100lb_cardstock")
        quantity: Number of sheets to print
        width_inches: Width in inches
        height_inches: Height in inches
        full_color: Whether full-color printing is needed
        rush_type: Optional rush type ("rush" or "express")
    
    Returns:
        Dictionary with price breakdown
    """
    pricing = load_pricing_config()
    
    # Validate paper stock
    if paper_stock not in pricing["base_prices"]:
        return {
            "error": f"Paper stock '{paper_stock}' not found in pricing database.",
            "available_stocks": list(pricing["base_prices"].keys())
        }
    
    base_prices = pricing["base_prices"][paper_stock]
    
    # Calculate quantity discount
    quantity_multiplier = 1.0
    for break_range, multiplier in pricing["quantity_breaks"].items():
        min_qty, max_qty = break_range.split("-")
        min_qty = int(min_qty)
        max_qty = int(max_qty.replace("+", "999999"))
        if min_qty <= quantity <= max_qty:
            quantity_multiplier = multiplier
            break
    
    # Calculate per-sheet cost
    per_sheet_cost = base_prices["per_sheet"]
    if full_color:
        per_sheet_cost += base_prices["color_surcharge"]
    
    # Apply quantity discount
    per_sheet_cost *= quantity_multiplier
    
    # Calculate total sheet cost
    total_sheet_cost = per_sheet_cost * quantity
    
    # Add setup fee
    setup_fee = base_prices["setup_fee"]
    
    # Apply rush surcharge if applicable
    rush_multiplier = 1.0
    if rush_type and rush_type in pricing["rush_surcharge"]:
        rush_multiplier = pricing["rush_surcharge"][rush_type]
    
    subtotal = (total_sheet_cost + setup_fee) * rush_multiplier
    
    # Calculate price per unit
    price_per_unit = subtotal / quantity if quantity > 0 else 0
    
    return {
        "paper_stock": paper_stock,
        "quantity": quantity,
        "dimensions": f"{width_inches}\" × {height_inches}\"",
        "per_sheet_cost": round(per_sheet_cost, 2),
        "total_sheet_cost": round(total_sheet_cost, 2),
        "setup_fee": round(setup_fee, 2),
        "rush_type": rush_type,
        "rush_multiplier": rush_multiplier,
        "quantity_discount": f"{(1 - quantity_multiplier) * 100:.0f}%",
        "subtotal": round(subtotal, 2),
        "price_per_unit": round(price_per_unit, 2),
        "total_price": round(subtotal, 2),
        "currency": "USD",
        "formatted_price": f"${subtotal:.2f}"
    }

