"""Layer 1: Spec-Check Guardrail - Validates order specifications against shop capabilities."""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List

class SpecCheckGuardrail:
    """Input guardrail that ensures customer orders are possible given shop capabilities."""
    
    def __init__(self):
        self.capabilities = self._load_capabilities()
        self.system_prompt_template = self._build_system_prompt()
    
    def _load_capabilities(self) -> Dict[str, Any]:
        """Load shop capabilities from config."""
        config_path = Path(__file__).parent.parent / "config" / "shop_capabilities.json"
        with open(config_path, "r") as f:
            return json.load(f)
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt with Shop Capability Manifest."""
        capabilities = self.capabilities
        
        prompt = """You are an AI assistant for a print shop. You must validate all orders against our shop capabilities.

SHOP CAPABILITY MANIFEST:

Paper Stocks Available:"""
        
        for stock_name, stock_info in capabilities["paper_stocks"].items():
            if stock_info["available"]:
                prompt += f"\n- {stock_name}:"
                prompt += f"\n  Colors: {', '.join(stock_info['colors'])}"
                prompt += f"\n  Finishes: {', '.join(stock_info['finish'])}"
                prompt += f"\n  White Ink Capable: {'Yes' if stock_info['white_ink_capable'] else 'No'}"
        
        prompt += f"""

Printing Capabilities:
- Full Color: {'Yes' if capabilities['printing_capabilities']['full_color'] else 'No'}
- Spot Color: {'Yes' if capabilities['printing_capabilities']['spot_color'] else 'No'}
- White Ink: {'Yes' if capabilities['printing_capabilities']['white_ink'] else 'No'}
- Metallic Inks: {'Yes' if capabilities['printing_capabilities']['metallic_inks'] else 'No'}
- Pantone Matching: {'Yes' if capabilities['printing_capabilities']['pantone_matching'] else 'No'}

File Requirements:
- Minimum Resolution: {capabilities['file_requirements']['min_resolution_dpi']} DPI
- Minimum Bleed: {capabilities['file_requirements']['min_bleed_mm']} mm
- Supported Formats: {', '.join(capabilities['file_requirements']['supported_formats'])}
- Color Space: {capabilities['file_requirements']['color_space']}

Size Limits:
- Maximum: {capabilities['size_limits']['max_width_inches']}\" × {capabilities['size_limits']['max_height_inches']}\"
- Minimum: {capabilities['size_limits']['min_width_inches']}\" × {capabilities['size_limits']['min_height_inches']}\"

CRITICAL RULES:
1. If a customer requests full-color printing on a dark paper stock (black, dark colors) without white ink capability, you MUST inform them this is not possible.
2. You must use the check_inventory tool to verify paper stock availability BEFORE accepting an order.
3. You must never accept orders that exceed size limits.
4. You must validate all file specifications before confirming an order.

"""
        return prompt
    
    def validate_order_spec(self, order_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate an order specification.
        
        Args:
            order_spec: Dictionary containing order details
        
        Returns:
            Dictionary with validation result
        """
        errors = []
        warnings = []
        
        # Check paper stock
        paper_stock = order_spec.get("paper_stock")
        color = order_spec.get("color", "white")
        finish = order_spec.get("finish", "matte")
        
        if not paper_stock:
            errors.append("Paper stock not specified")
        else:
            # This would typically call check_inventory tool
            if paper_stock not in self.capabilities["paper_stocks"]:
                errors.append(f"Paper stock '{paper_stock}' not available")
            else:
                stock_info = self.capabilities["paper_stocks"][paper_stock]
                if color not in stock_info["colors"]:
                    errors.append(f"Color '{color}' not available for {paper_stock}")
                if finish not in stock_info["finish"]:
                    errors.append(f"Finish '{finish}' not available for {paper_stock}")
        
        # Check printing capabilities
        if order_spec.get("full_color") and order_spec.get("dark_paper"):
            if not self.capabilities["printing_capabilities"]["white_ink"]:
                errors.append("Full-color printing on dark paper requires white ink, which is not available")
        
        # Check size limits
        width = order_spec.get("width_inches")
        height = order_spec.get("height_inches")
        if width and height:
            max_w = self.capabilities["size_limits"]["max_width_inches"]
            max_h = self.capabilities["size_limits"]["max_height_inches"]
            min_w = self.capabilities["size_limits"]["min_width_inches"]
            min_h = self.capabilities["size_limits"]["min_height_inches"]
            
            if width > max_w or height > max_h:
                errors.append(f"Size {width}\" × {height}\" exceeds maximum {max_w}\" × {max_h}\"")
            if width < min_w or height < min_h:
                errors.append(f"Size {width}\" × {height}\" is below minimum {min_w}\" × {min_h}\"")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def get_system_prompt(self) -> str:
        """Get the system prompt with capability manifest."""
        return self.system_prompt_template





