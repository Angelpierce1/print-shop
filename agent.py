"""
ReAct Agent for Print Shop Order Processing
Implements the three-layer guardrail system with tool-based reasoning.
"""

import os
import json
import re
from shop_capabilities import check_spec_compatibility
from tools import check_inventory, check_resolution, calculate_price

# System prompt for the agent
SYSTEM_PROMPT = """
You are an AI Order Guardrail Agent for Tim's Print Shop. Your job is to validate orders
and catch errors before they reach human technicians.

You have access to three tools:
1. check_inventory(paper_type, quantity) - Check if paper is in stock
2. check_resolution(file_path, width_inch, height_inch) - Check image DPI quality
3. calculate_price(size, paper_type, quantity) - Get official pricing

CRITICAL RULES:
- NEVER estimate or guess prices. ONLY use the calculate_price tool.
- If you mention a price without calling calculate_price, that's a HALLUCINATION.
- Always validate orders through all three guardrail layers:
  Layer 1: Spec-Check (shop capabilities)
  Layer 2: Pre-flight (file resolution)
  Layer 3: Final Quote (must use calculate_price tool)

When an order fails validation, clearly explain what's wrong and ask the user to fix it.
"""


class PrintShopAgent:
    """
    ReAct-style agent for processing print orders with guardrails.
    """
    
    def __init__(self):
        self.tool_calls = []
        self.reasoning_steps = []
    
    def _extract_tool_call(self, text):
        """Extract tool calls from agent response (format: TOOL_NAME(arg1, arg2))"""
        pattern = r'(\w+)\(([^)]+)\)'
        matches = re.findall(pattern, text)
        return matches
    
    def _parse_tool_args(self, args_str):
        """Parse tool arguments from string"""
        # Simple parsing - handles strings and numbers
        args = []
        current = ""
        in_quotes = False
        
        for char in args_str:
            if char == '"' or char == "'":
                in_quotes = not in_quotes
            elif char == ',' and not in_quotes:
                args.append(current.strip().strip('"').strip("'"))
                current = ""
                continue
            current += char
        
        if current:
            args.append(current.strip().strip('"').strip("'"))
        
        return args
    
    def process_order(self, order_data):
        """
        Main order processing function with three-layer guardrails.
        
        Args:
            order_data: dict with keys:
                - email: str
                - name: str (optional)
                - size: str (e.g., "8x10")
                - paper: str (optional)
                - quantity: int (default 1)
                - file_path: str (path to uploaded file)
                - filename: str
        
        Returns:
            dict with validation results and response
        """
        self.tool_calls = []
        self.reasoning_steps = []
        
        # Extract order details
        size = order_data.get('size', '')
        paper = order_data.get('paper', '100lb Matte')  # Default
        quantity = order_data.get('quantity', 1)
        file_path = order_data.get('file_path', '')
        filename = order_data.get('filename', '')
        
        # Parse size
        size_parts = size.split(',')
        if len(size_parts) == 2:
            width_inch, height_inch = map(float, size_parts)
            size_name = f"{int(width_inch)}x{int(height_inch)}"
        else:
            # Try to parse from size string like "8x10"
            size_match = re.match(r'(\d+(?:\.\d+)?)x(\d+(?:\.\d+)?)', size)
            if size_match:
                width_inch = float(size_match.group(1))
                height_inch = float(size_match.group(2))
                size_name = size
            else:
                return {
                    "valid": False,
                    "error": "Invalid size format. Expected format: 'width,height' or '8x10'",
                    "reasoning": self.reasoning_steps
                }
        
        # ============================================
        # LAYER 1: SPEC-CHECK GUARDRAIL (Input)
        # ============================================
        self.reasoning_steps.append("🔍 Layer 1: Checking order specifications against shop capabilities...")
        
        order_spec = {
            'paper': paper,
            'size': size_name,
            'quantity': quantity
        }
        
        spec_check = check_spec_compatibility(order_spec)
        
        if not spec_check["valid"]:
            return {
                "valid": False,
                "layer": "spec_check",
                "errors": spec_check["errors"],
                "warnings": spec_check["warnings"],
                "message": "Order rejected: " + "; ".join(spec_check["errors"]),
                "reasoning": self.reasoning_steps
            }
        
        if spec_check["warnings"]:
            self.reasoning_steps.append(f"⚠️ Warnings: {', '.join(spec_check['warnings'])}")
        
        self.reasoning_steps.append("✅ Layer 1 passed: Order specifications are valid.")
        
        # ============================================
        # LAYER 2: PRE-FLIGHT GUARDRAIL (Action)
        # ============================================
        self.reasoning_steps.append("🔍 Layer 2: Checking file resolution (pre-flight)...")
        
        if not file_path or not os.path.exists(file_path):
            return {
                "valid": False,
                "layer": "preflight",
                "error": "File not found. Please upload a valid file.",
                "reasoning": self.reasoning_steps
            }
        
        # Call check_resolution tool
        resolution_result = check_resolution(file_path, width_inch, height_inch)
        self.tool_calls.append({
            "tool": "check_resolution",
            "args": [file_path, width_inch, height_inch],
            "result": resolution_result
        })
        
        if "error" in resolution_result:
            return {
                "valid": False,
                "layer": "preflight",
                "error": resolution_result["error"],
                "reasoning": self.reasoning_steps
            }
        
        if not resolution_result["valid"]:
            return {
                "valid": False,
                "layer": "preflight",
                "error": resolution_result["message"],
                "dpi": resolution_result["dpi"],
                "message": f"File quality too low: {resolution_result['message']}. Please upload a higher resolution image.",
                "reasoning": self.reasoning_steps
            }
        
        self.reasoning_steps.append(f"✅ Layer 2 passed: {resolution_result['message']}")
        
        # ============================================
        # LAYER 3: FINAL QUOTE GUARDRAIL (Output)
        # ============================================
        self.reasoning_steps.append("🔍 Layer 3: Calculating official price...")
        
        # Check inventory
        inventory_result = check_inventory(paper, quantity)
        self.tool_calls.append({
            "tool": "check_inventory",
            "args": [paper, quantity],
            "result": inventory_result
        })
        
        if not inventory_result["available"]:
            return {
                "valid": False,
                "layer": "inventory",
                "error": inventory_result["message"],
                "available_options": inventory_result.get("available_options", []),
                "reasoning": self.reasoning_steps
            }
        
        # Calculate price using official tool
        price_result = calculate_price(size_name, paper, quantity)
        self.tool_calls.append({
            "tool": "calculate_price",
            "args": [size_name, paper, quantity],
            "result": price_result
        })
        
        self.reasoning_steps.append(f"✅ Layer 3 passed: Price calculated: {price_result['formatted_price']}")
        
        # ============================================
        # OUTPUT GUARDRAIL: Verify no price hallucination
        # ============================================
        # This ensures the price came from the tool, not from the agent's imagination
        if not any(call["tool"] == "calculate_price" for call in self.tool_calls):
            return {
                "valid": False,
                "layer": "output_guardrail",
                "error": "PRICE HALLUCINATION DETECTED: Agent attempted to provide price without using calculate_price tool.",
                "reasoning": self.reasoning_steps
            }
        
        # ============================================
        # SUCCESS: All guardrails passed
        # ============================================
        return {
            "valid": True,
            "message": "Order validated successfully! All guardrails passed.",
            "order_summary": {
                "size": size_name,
                "dimensions": f"{width_inch}\" x {height_inch}\"",
                "paper": inventory_result.get("paper", paper),
                "quantity": quantity,
                "file_quality": {
                    "dpi": resolution_result["dpi"],
                    "quality": resolution_result["quality"],
                    "pixel_dimensions": resolution_result["pixel_dimensions"]
                },
                "price": price_result["formatted_price"],
                "price_breakdown": {
                    "per_sheet": f"${price_result['per_sheet_price']:.2f}",
                    "subtotal": f"${price_result['subtotal']:.2f}",
                    "discount": f"{price_result['discount_rate']*100:.0f}%",
                    "total": price_result["formatted_price"]
                }
            },
            "tool_calls": self.tool_calls,
            "reasoning": self.reasoning_steps
        }

