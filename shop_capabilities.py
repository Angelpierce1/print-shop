"""
Shop Capability Manifest
This defines what the print shop CAN and CANNOT do.
Used by Layer 1: Spec-Check Guardrail
"""

SHOP_CAPABILITIES = {
    "paper_stocks": {
        "available": [
            "80lb Glossy",
            "100lb Matte",
            "110lb Cardstock",
            "65lb Text",
            "80lb Text"
        ],
        "not_available": [
            "Black cardstock with white ink",
            "Metallic paper",
            "Foil stamping",
            "Embossing"
        ]
    },
    "ink_capabilities": {
        "standard_colors": True,  # CMYK printing
        "white_ink": False,  # Cannot print white ink
        "spot_colors": False,  # No Pantone spot colors
        "metallic_ink": False,
        "uv_coating": False
    },
    "print_sizes": {
        "min_size": (3, 5),  # inches
        "max_size": (13, 19),  # inches
        "standard_sizes": [
            "3x5", "4x6", "5x7", "8x10", "8.5x11",
            "11x14", "11x17", "12x18", "13x19"
        ]
    },
    "file_requirements": {
        "min_dpi": 225,
        "recommended_dpi": 300,
        "accepted_formats": ["JPG", "PNG", "PDF", "HEIC"],
        "color_space": "CMYK or RGB (will convert)",
        "bleed_required": False,  # Not required but recommended
        "safe_zone": "0.125 inches from edges"
    },
    "special_services": {
        "full_bleed": True,
        "perforation": False,
        "die_cutting": False,
        "folding": True,
        "binding": False,
        "lamination": False
    },
    "restrictions": [
        "Cannot print white ink on dark paper",
        "Cannot print metallic or foil effects",
        "Maximum size: 13x19 inches",
        "Minimum DPI: 225 (300 recommended)",
        "No spot colors or Pantone matching"
    ]
}

def check_spec_compatibility(order_spec):
    """
    Layer 1: Spec-Check Guardrail
    Validates if the order request matches shop capabilities.
    
    Args:
        order_spec: dict with keys like 'paper', 'size', 'ink_type', etc.
    
    Returns:
        dict with 'valid': bool, 'errors': list, 'warnings': list
    """
    errors = []
    warnings = []
    
    # Check paper stock
    if 'paper' in order_spec:
        paper = order_spec['paper'].lower()
        if any(restricted in paper for restricted in ['black', 'metallic', 'foil']):
            errors.append(f"Paper type '{order_spec['paper']}' is not available. We don't support black cardstock with white ink, metallic, or foil papers.")
        elif paper not in [p.lower() for p in SHOP_CAPABILITIES["paper_stocks"]["available"]]:
            warnings.append(f"Paper '{order_spec['paper']}' may not be in stock. Standard options: {', '.join(SHOP_CAPABILITIES['paper_stocks']['available'])}")
    
    # Check ink requirements
    if 'ink_type' in order_spec:
        ink = order_spec['ink_type'].lower()
        if 'white' in ink and 'black' in order_spec.get('paper', '').lower():
            errors.append("Cannot print white ink on dark paper. We don't have white ink capabilities.")
        if 'metallic' in ink or 'foil' in ink:
            errors.append("Metallic ink and foil printing are not available.")
    
    # Check size
    if 'size' in order_spec:
        size = order_spec['size']
        if isinstance(size, str) and 'x' in size:
            try:
                width, height = map(float, size.split('x'))
                min_w, min_h = SHOP_CAPABILITIES["print_sizes"]["min_size"]
                max_w, max_h = SHOP_CAPABILITIES["print_sizes"]["max_size"]
                if width < min_w or height < min_h or width > max_w or height > max_h:
                    errors.append(f"Size {size}\" is outside our range ({min_w}x{min_h}\" to {max_w}x{max_h}\").")
            except:
                pass
    
    # Check special services
    if 'special_services' in order_spec:
        for service in order_spec['special_services']:
            if not SHOP_CAPABILITIES["special_services"].get(service, False):
                errors.append(f"Service '{service}' is not available.")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "capabilities": SHOP_CAPABILITIES
    }

