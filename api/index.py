"""Vercel serverless function for Print Shop AI Order Guardrail API."""

import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.react_agent import ReActAgent
from tools.inventory_tool import check_inventory
from tools.resolution_tool import check_resolution
from tools.pricing_tool import calculate_price
from guardrails.spec_check_guardrail import SpecCheckGuardrail
from guardrails.preflight_guardrail import PreflightGuardrail
from guardrails.quote_guardrail import QuoteGuardrail


def handler(req):
    """Main handler for Vercel serverless function."""
    
    # Handle CORS
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }
    
    # Handle OPTIONS for CORS
    if req.method == "OPTIONS":
        return {"statusCode": 200, "headers": headers, "body": ""}
    
    try:
        # Parse request body
        body = {}
        if req.method == "POST":
            if hasattr(req, 'body') and req.body:
                try:
                    if isinstance(req.body, str):
                        body = json.loads(req.body)
                    else:
                        body = req.body
                except:
                    body = {}
        
        # Get action from body or query string
        action = body.get("action")
        if not action and hasattr(req, 'query') and req.query:
            action = req.query.get("action", "info")
        else:
            action = action or "info"
        
        # Route to appropriate handler
        if action == "process_order":
            result = handle_process_order(body)
        elif action == "check_inventory":
            result = handle_check_inventory(body)
        elif action == "check_resolution":
            result = handle_check_resolution(body)
        elif action == "calculate_price":
            result = handle_calculate_price(body)
        elif action == "test_guardrails":
            result = handle_test_guardrails()
        else:
            result = {
                "success": True,
                "message": "Print Shop AI Order Guardrail API",
                "available_actions": [
                    "process_order",
                    "check_inventory", 
                    "check_resolution",
                    "calculate_price",
                    "test_guardrails"
                ],
                "usage": {
                    "method": "POST",
                    "example": {
                        "action": "calculate_price",
                        "paper_stock": "100lb_cardstock",
                        "quantity": 500,
                        "width_inches": 3.5,
                        "height_inches": 2.0
                    }
                }
            }
        
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps(result, default=str)
        }
    
    except Exception as e:
        import traceback
        error_msg = str(e)
        # Don't expose full traceback in production, but include it for debugging
        traceback_info = traceback.format_exc() if "dev" in str(req.path).lower() else None
        
        error_response = {
            "success": False,
            "error": error_msg
        }
        if traceback_info:
            error_response["traceback"] = traceback_info
        
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps(error_response, default=str)
        }


def handle_process_order(body):
    """Handle process_order action."""
    user_query = body.get("query", "")
    file_path = body.get("file_path")
    
    agent = ReActAgent()
    result = agent.process_order(user_query, file_path)
    
    return {
        "success": True,
        "result": result
    }


def handle_check_inventory(body):
    """Handle check_inventory action."""
    paper_stock = body.get("paper_stock")
    color = body.get("color", "white")
    finish = body.get("finish", "matte")
    
    if not paper_stock:
        return {
            "success": False,
            "error": "paper_stock is required"
        }
    
    result = check_inventory(paper_stock, color, finish)
    return {
        "success": True,
        "result": result
    }


def handle_check_resolution(body):
    """Handle check_resolution action."""
    file_path = body.get("file_path")
    
    if not file_path:
        return {
            "success": False,
            "error": "file_path is required"
        }
    
    result = check_resolution(file_path)
    return {
        "success": True,
        "result": result
    }


def handle_calculate_price(body):
    """Handle calculate_price action."""
    paper_stock = body.get("paper_stock")
    quantity = body.get("quantity")
    width_inches = body.get("width_inches")
    height_inches = body.get("height_inches")
    full_color = body.get("full_color", True)
    rush_type = body.get("rush_type")
    
    if not all([paper_stock, quantity, width_inches, height_inches]):
        return {
            "success": False,
            "error": "paper_stock, quantity, width_inches, and height_inches are required"
        }
    
    result = calculate_price(
        paper_stock=paper_stock,
        quantity=quantity,
        width_inches=width_inches,
        height_inches=height_inches,
        full_color=full_color,
        rush_type=rush_type
    )
    
    return {
        "success": True,
        "result": result
    }


def handle_test_guardrails():
    """Handle test_guardrails action."""
    spec_guardrail = SpecCheckGuardrail()
    preflight_guardrail = PreflightGuardrail()
    quote_guardrail = QuoteGuardrail()
    
    # Test Layer 1
    test_order = {
        "paper_stock": "100lb_cardstock",
        "color": "black",
        "finish": "matte",
        "full_color": True,
        "dark_paper": True
    }
    layer1_result = spec_guardrail.validate_order_spec(test_order)
    
    # Test Layer 3
    test_response = "The price for your order will be $125.50"
    layer3_result = quote_guardrail.validate_response(test_response, [])
    
    return {
        "success": True,
        "layer1_spec_check": layer1_result,
        "layer3_quote_guardrail": layer3_result,
        "layer2_preflight": "Requires file to test"
    }
