"""ReAct (Reasoning + Acting) Agent Loop for Print Shop Order Processing."""

from typing import Dict, Any, List, Optional, Callable
import json
from pathlib import Path

# Handle both relative and absolute imports
try:
    from tools.inventory_tool import check_inventory
    from tools.resolution_tool import check_resolution
    from tools.pricing_tool import calculate_price
    from guardrails.spec_check_guardrail import SpecCheckGuardrail
    from guardrails.preflight_guardrail import PreflightGuardrail
    from guardrails.quote_guardrail import QuoteGuardrail
except ImportError:
    # Try relative imports
    from ..tools.inventory_tool import check_inventory
    from ..tools.resolution_tool import check_resolution
    from ..tools.pricing_tool import calculate_price
    from ..guardrails.spec_check_guardrail import SpecCheckGuardrail
    from ..guardrails.preflight_guardrail import PreflightGuardrail
    from ..guardrails.quote_guardrail import QuoteGuardrail


class ReActAgent:
    """
    ReAct loop agent for processing print shop orders with multi-layered guardrails.
    
    The agent follows a Think -> Act -> Observe loop:
    1. Think: Analyze the current situation
    2. Act: Use a tool or provide final answer
    3. Observe: Process tool results and continue
    """
    
    def __init__(self):
        self.spec_check = SpecCheckGuardrail()
        self.preflight = PreflightGuardrail()
        self.quote_guardrail = QuoteGuardrail()
        
        # Available tools
        self.tools = {
            "check_inventory": {
                "function": check_inventory,
                "description": "Check if a paper stock, color, and finish combination is available",
                "parameters": ["paper_stock", "color", "finish"]
            },
            "check_resolution": {
                "function": check_resolution,
                "description": "Check the resolution (DPI) of an image or PDF file",
                "parameters": ["file_path"]
            },
            "calculate_price": {
                "function": calculate_price,
                "description": "Calculate the price for a print order (MUST use for all prices)",
                "parameters": ["paper_stock", "quantity", "width_inches", "height_inches", 
                             "full_color", "rush_type"]
            }
        }
        
        self.tool_calls_history: List[Dict[str, Any]] = []
        self.observation_history: List[str] = []
    
    def get_system_prompt(self) -> str:
        """Get the system prompt with shop capabilities."""
        base_prompt = self.spec_check.get_system_prompt()
        
        tools_description = """

AVAILABLE TOOLS:

1. check_inventory(paper_stock, color, finish)
   - Check if a paper stock combination is available
   - Use this BEFORE accepting any order with specific paper requirements

2. check_resolution(file_path)
   - Check the DPI/resolution of a file (PDF or image)
   - Use this when a customer uploads a file
   - Minimum required: 300 DPI

3. calculate_price(paper_stock, quantity, width_inches, height_inches, full_color, rush_type)
   - Calculate the price for a print order
   - YOU MUST USE THIS TOOL for ANY price quote
   - NEVER estimate or guess prices
   - Parameters:
     * paper_stock: e.g., "100lb_cardstock"
     * quantity: number of sheets
     * width_inches: width in inches
     * height_inches: height in inches
     * full_color: True/False (default: True)
     * rush_type: "rush", "express", or None

REACT LOOP PROCESS:
1. Think: Analyze what you need to do
2. Act: Use a tool OR provide final answer
3. Observe: Process the tool result and continue if needed

CRITICAL RULES:
- Always validate orders using check_inventory first
- Always check file resolution using check_resolution
- NEVER provide a price without using calculate_price tool
- If any validation fails, ask the customer for corrections
"""
        
        return base_prompt + tools_description
    
    def call_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        Call a tool by name.
        
        Args:
            tool_name: Name of the tool to call
            **kwargs: Arguments to pass to the tool
        
        Returns:
            Tool result dictionary
        """
        if tool_name not in self.tools:
            return {
                "error": f"Tool '{tool_name}' not found",
                "available_tools": list(self.tools.keys())
            }
        
        tool = self.tools[tool_name]
        
        try:
            result = tool["function"](**kwargs)
            
            # Record tool call
            self.tool_calls_history.append({
                "tool_name": tool_name,
                "arguments": kwargs,
                "result": result
            })
            
            return result
        except Exception as e:
            return {
                "error": f"Error calling tool {tool_name}: {str(e)}"
            }
    
    def process_order(self, user_query: str, file_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Process an order through the ReAct loop.
        
        This is a simplified version. In production, you'd integrate with an LLM.
        
        Args:
            user_query: The customer's order request
            file_path: Optional path to uploaded file
        
        Returns:
            Dictionary with processing result
        """
        # Layer 1: Spec-Check Guardrail (would be applied via system prompt in LLM integration)
        # For now, we'll validate in the processing logic
        
        steps = []
        current_step = 1
        
        # Step 1: Parse order (in production, LLM would do this)
        # For PoC, we assume order details are extracted
        
        # Step 2: Check inventory if paper specs are mentioned
        # This would be triggered by the LLM calling the tool
        
        # Step 3: Check file resolution if file is provided
        if file_path:
            steps.append({
                "step": current_step,
                "action": "preflight_check",
                "tool": "check_resolution"
            })
            current_step += 1
            
            resolution_result = self.call_tool("check_resolution", file_path=file_path)
            preflight_result = self.preflight.validate_file(file_path)
            
            if not preflight_result["valid"]:
                return {
                    "status": "rejected",
                    "reason": "preflight_failed",
                    "details": preflight_result,
                    "message": f"File validation failed: {preflight_result.get('error', 'Resolution too low')}. "
                              f"Please provide a file with at least 300 DPI resolution.",
                    "steps": steps
                }
        
        # Step 4: Calculate price if all validations pass
        # This would be triggered by the LLM calling the tool
        
        return {
            "status": "processing",
            "message": "Order processing (simplified PoC version - integrate with LLM for full functionality)",
            "steps": steps,
            "tool_calls": self.tool_calls_history
        }
    
    def validate_final_response(self, response_text: str) -> Dict[str, Any]:
        """
        Validate the final response using Layer 3 guardrail.
        
        Args:
            response_text: The agent's response text
        
        Returns:
            Validation result
        """
        return self.quote_guardrail.validate_response(
            response_text, 
            self.tool_calls_history
        )

