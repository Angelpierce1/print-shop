"""Vercel serverless function for Print Shop AI Order Guardrail API."""

import json
import sys
import traceback
from pathlib import Path

# Add parent directory to path
try:
    parent_dir = str(Path(__file__).parent.parent)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
except:
    pass

# Try to import modules, but handle gracefully if they fail
IMPORTS_OK = False
IMPORT_ERROR = None
MODULES = {}

try:
    from tools.inventory_tool import check_inventory
    MODULES['check_inventory'] = check_inventory
    from tools.pricing_tool import calculate_price
    MODULES['calculate_price'] = calculate_price
    from guardrails.spec_check_guardrail import SpecCheckGuardrail
    MODULES['SpecCheckGuardrail'] = SpecCheckGuardrail
    from guardrails.quote_guardrail import QuoteGuardrail
    MODULES['QuoteGuardrail'] = QuoteGuardrail
    
    # Optional imports that might fail
    try:
        from tools.resolution_tool import check_resolution
        MODULES['check_resolution'] = check_resolution
    except Exception as e:
        MODULES['check_resolution'] = None
        MODULES['resolution_error'] = str(e)
    
    try:
        from guardrails.preflight_guardrail import PreflightGuardrail
        MODULES['PreflightGuardrail'] = PreflightGuardrail
    except Exception as e:
        MODULES['PreflightGuardrail'] = None
        MODULES['preflight_error'] = str(e)
    
    try:
        from agent.react_agent import ReActAgent
        MODULES['ReActAgent'] = ReActAgent
    except Exception as e:
        MODULES['ReActAgent'] = None
        MODULES['agent_error'] = str(e)
    
    IMPORTS_OK = True
except Exception as e:
    IMPORT_ERROR = str(e)
    IMPORT_TRACEBACK = traceback.format_exc()


def handler(req):
    """Main handler for Vercel serverless function."""
    
    # Handle CORS
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }
    
    try:
        # Get request method safely
        method = 'GET'
        if hasattr(req, 'method'):
            method = req.method
        elif isinstance(req, dict) and 'method' in req:
            method = req['method']
        
        # Handle OPTIONS for CORS
        if method == "OPTIONS":
            return {
                "statusCode": 200,
                "headers": headers,
                "body": ""
            }
        
        # If imports failed, return detailed error info
        if not IMPORTS_OK:
            return {
                "statusCode": 500,
                "headers": headers,
                "body": json.dumps({
                    "success": False,
                    "error": "Import error",
                    "details": IMPORT_ERROR,
                    "traceback": IMPORT_TRACEBACK if 'IMPORT_TRACEBACK' in globals() else None,
                    "message": "Check Vercel function logs. Some dependencies may be missing."
                }, default=str)
            }
        
        # Parse request body
        body = {}
        if method == "POST":
            req_body = None
            if hasattr(req, 'body'):
                req_body = req.body
            elif isinstance(req, dict) and 'body' in req:
                req_body = req['body']
            
            if req_body:
                try:
                    if isinstance(req_body, str):
                        body = json.loads(req_body)
                    elif isinstance(req_body, dict):
                        body = req_body
                except:
                    body = {}
        
        # Get action from body or query string
        action = body.get("action", "info")
        if not action or action == "info":
            query = {}
            if hasattr(req, 'query'):
                query = req.query if isinstance(req.query, dict) else {}
            elif isinstance(req, dict) and 'query' in req:
                query = req['query'] if isinstance(req['query'], dict) else {}
            
            if query and 'action' in query:
                action = query['action']
        
        # Route to appropriate handler
        if action == "check_inventory" and MODULES.get('check_inventory'):
            result = handle_check_inventory(body)
        elif action == "calculate_price" and MODULES.get('calculate_price'):
            result = handle_calculate_price(body)
        elif action == "check_resolution" and MODULES.get('check_resolution'):
            result = handle_check_resolution(body)
        elif action == "test_guardrails":
            result = handle_test_guardrails()
        elif action == "process_order" and MODULES.get('ReActAgent'):
            result = handle_process_order(body)
        else:
            # Return info about available actions
            available = []
            if MODULES.get('check_inventory'):
                available.append("check_inventory")
            if MODULES.get('calculate_price'):
                available.append("calculate_price")
            if MODULES.get('check_resolution'):
                available.append("check_resolution")
            if MODULES.get('SpecCheckGuardrail'):
                available.append("test_guardrails")
            if MODULES.get('ReActAgent'):
                available.append("process_order")
            
            result = {
                "success": True,
                "message": "Print Shop AI Order Guardrail API",
                "available_actions": available,
                "modules_loaded": {
                    "check_inventory": MODULES.get('check_inventory') is not None,
                    "calculate_price": MODULES.get('calculate_price') is not None,
                    "check_resolution": MODULES.get('check_resolution') is not None,
                    "guardrails": MODULES.get('SpecCheckGuardrail') is not None,
                    "agent": MODULES.get('ReActAgent') is not None
                },
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
        error_traceback = traceback.format_exc()
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__,
                "traceback": error_traceback
            }, default=str)
        }


def handle_process_order(body):
    """Handle process_order action."""
    if not MODULES.get('ReActAgent'):
        return {"success": False, "error": "ReActAgent not available"}
    
    user_query = body.get("query", "")
    file_path = body.get("file_path")
    
    agent = MODULES['ReActAgent']()
    result = agent.process_order(user_query, file_path)
    
    return {
        "success": True,
        "result": result
    }


def handle_check_inventory(body):
    """Handle check_inventory action."""
    if not MODULES.get('check_inventory'):
        return {"success": False, "error": "check_inventory not available"}
    
    paper_stock = body.get("paper_stock")
    color = body.get("color", "white")
    finish = body.get("finish", "matte")
    
    if not paper_stock:
        return {
            "success": False,
            "error": "paper_stock is required"
        }
    
    result = MODULES['check_inventory'](paper_stock, color, finish)
    return {
        "success": True,
        "result": result
    }


def handle_check_resolution(body):
    """Handle check_resolution action."""
    if not MODULES.get('check_resolution'):
        return {
            "success": False,
            "error": "check_resolution not available",
            "details": MODULES.get('resolution_error', 'Unknown error')
        }
    
    file_path = body.get("file_path")
    
    if not file_path:
        return {
            "success": False,
            "error": "file_path is required"
        }
    
    result = MODULES['check_resolution'](file_path)
    return {
        "success": True,
        "result": result
    }


def handle_calculate_price(body):
    """Handle calculate_price action."""
    if not MODULES.get('calculate_price'):
        return {"success": False, "error": "calculate_price not available"}
    
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
    
    result = MODULES['calculate_price'](
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
    if not MODULES.get('SpecCheckGuardrail'):
        return {"success": False, "error": "Guardrails not available"}
    
    spec_guardrail = MODULES['SpecCheckGuardrail']()
    quote_guardrail = MODULES.get('QuoteGuardrail')
    
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
    layer3_result = None
    if quote_guardrail:
        test_response = "The price for your order will be $125.50"
        layer3_result = quote_guardrail.validate_response(test_response, [])
    
    return {
        "success": True,
        "layer1_spec_check": layer1_result,
        "layer3_quote_guardrail": layer3_result,
        "layer2_preflight": "Requires file to test"
    }
