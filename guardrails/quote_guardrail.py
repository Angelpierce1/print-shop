"""Layer 3: Final Quote Guardrail - Prevents price hallucinations."""

import re
from typing import Dict, Any, Optional, List

class QuoteGuardrail:
    """Output guardrail that prevents the agent from generating prices without using the pricing tool."""
    
    def __init__(self):
        self.price_pattern = re.compile(r'\$[\d,]+\.?\d*')
        self.allowed_price_source = "calculate_price_tool"
    
    def validate_response(self, response_text: str, tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate that any prices in the response came from the pricing tool.
        
        This is Layer 3: Final Quote Guardrail
        
        Args:
            response_text: The agent's response text
            tool_calls: List of tool calls made during this interaction
        
        Returns:
            Dictionary with validation result
        """
        # Find all price mentions in the response
        price_mentions = self.price_pattern.findall(response_text)
        
        if not price_mentions:
            # No prices mentioned, that's fine
            return {
                "valid": True,
                "guardrail": "quote",
                "layer": 3,
                "prices_found": []
            }
        
        # Check if calculate_price tool was called
        pricing_tool_used = any(
            call.get("tool_name") == "calculate_price" 
            or call.get("name") == "calculate_price"
            for call in tool_calls
        )
        
        if not pricing_tool_used:
            return {
                "valid": False,
                "error": "Price mentioned in response but calculate_price tool was not used",
                "guardrail": "quote",
                "layer": 3,
                "prices_found": price_mentions,
                "violation": "PRICE_HALLUCINATION"
            }
        
        # Tool was used, response is valid
        return {
            "valid": True,
            "guardrail": "quote",
            "layer": 3,
            "prices_found": price_mentions,
            "pricing_tool_used": True
        }
    
    def should_intervene(self, response_text: str, tool_calls: List[Dict[str, Any]]) -> bool:
        """
        Determine if the guardrail should intervene (block the response).
        
        Returns:
            True if intervention is needed, False otherwise
        """
        result = self.validate_response(response_text, tool_calls)
        return not result.get("valid", False)
    
    def get_intervention_message(self) -> str:
        """Get the message to show when intervention is needed."""
        return (
            "⚠️ GUARDRAIL VIOLATION: Price mentioned without using the calculate_price tool. "
            "All prices must come from the official pricing tool. Please recalculate using the tool."
        )

