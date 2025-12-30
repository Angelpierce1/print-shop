"""Layer 2: Pre-flight Guardrail - Validates technical file specifications."""

from pathlib import Path
from typing import Dict, Any, Optional

# Handle both relative and absolute imports
try:
    from tools.resolution_tool import check_resolution
except ImportError:
    from ..tools.resolution_tool import check_resolution

class PreflightGuardrail:
    """Action guardrail that verifies technical files (PDFs/Images) before processing."""
    
    def __init__(self):
        self.min_resolution_dpi = 300  # Default, loaded from config in practice
    
    def validate_file(self, file_path: str) -> Dict[str, Any]:
        """
        Validate a file using the pre-flight guardrail.
        
        This is called whenever the agent needs to check a file.
        
        Args:
            file_path: Path to the file to validate
        
        Returns:
            Dictionary with validation result
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            return {
                "valid": False,
                "error": f"File not found: {file_path}",
                "guardrail": "preflight",
                "layer": 2
            }
        
        # Use the resolution tool to check file
        resolution_result = check_resolution(file_path)
        
        if not resolution_result.get("valid", False):
            return {
                "valid": False,
                "error": resolution_result.get("error", "File validation failed"),
                "resolution_dpi": resolution_result.get("resolution_dpi"),
                "guardrail": "preflight",
                "layer": 2,
                "details": resolution_result
            }
        
        # Additional validations could go here:
        # - Bleed check
        # - Color space validation
        # - File size check
        
        return {
            "valid": True,
            "guardrail": "preflight",
            "layer": 2,
            "resolution_dpi": resolution_result.get("resolution_dpi"),
            "details": resolution_result
        }
    
    def should_intervene(self, file_path: str) -> bool:
        """
        Determine if the guardrail should intervene (stop the order).
        
        Returns:
            True if intervention is needed, False otherwise
        """
        result = self.validate_file(file_path)
        return not result.get("valid", False)

