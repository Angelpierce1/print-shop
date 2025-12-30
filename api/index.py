"""Vercel serverless function for Print Shop AI Order Guardrail API using FastAPI."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
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

# Initialize FastAPI app - MUST be named 'app' for Vercel
app = FastAPI(title="Print Shop AI Order Guardrail API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Try to import modules
MODULES = {}
IMPORTS_OK = False
IMPORT_ERROR = None

try:
    from tools.inventory_tool import check_inventory
    MODULES['check_inventory'] = check_inventory
    from tools.pricing_tool import calculate_price
    MODULES['calculate_price'] = calculate_price
    from guardrails.spec_check_guardrail import SpecCheckGuardrail
    MODULES['SpecCheckGuardrail'] = SpecCheckGuardrail
    from guardrails.quote_guardrail import QuoteGuardrail
    MODULES['QuoteGuardrail'] = QuoteGuardrail
    
    # Optional imports
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
    
    try:
        from agent.react_agent import ReActAgent
        MODULES['ReActAgent'] = ReActAgent
    except Exception as e:
        MODULES['ReActAgent'] = None
    
    IMPORTS_OK = True
except Exception as e:
    IMPORT_ERROR = str(e)
    IMPORT_TRACEBACK = traceback.format_exc()


# Pydantic models for request validation
class ProcessOrderRequest(BaseModel):
    query: str
    file_path: Optional[str] = None


class CheckInventoryRequest(BaseModel):
    paper_stock: str
    color: str = "white"
    finish: str = "matte"


class CheckResolutionRequest(BaseModel):
    file_path: str


class CalculatePriceRequest(BaseModel):
    paper_stock: str
    quantity: int
    width_inches: float
    height_inches: float
    full_color: bool = True
    rush_type: Optional[str] = None


@app.get("/")
@app.get("/api")
@app.get("/api/index")
async def root():
    """Root endpoint - returns API info."""
    if not IMPORTS_OK:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Import error",
                "details": IMPORT_ERROR,
                "traceback": IMPORT_TRACEBACK if 'IMPORT_TRACEBACK' in globals() else None
            }
        )
    
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
    
    return {
        "success": True,
        "message": "Print Shop AI Order Guardrail API",
        "available_actions": available,
        "modules_loaded": {
            "check_inventory": MODULES.get('check_inventory') is not None,
            "calculate_price": MODULES.get('calculate_price') is not None,
            "check_resolution": MODULES.get('check_resolution') is not None,
            "guardrails": MODULES.get('SpecCheckGuardrail') is not None,
            "agent": MODULES.get('ReActAgent') is not None
        }
    }


@app.post("/api/process_order")
async def process_order(request: ProcessOrderRequest):
    """Process an order through the agent."""
    if not MODULES.get('ReActAgent'):
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": "ReActAgent not available"}
        )
    
    agent = MODULES['ReActAgent']()
    result = agent.process_order(request.query, request.file_path)
    
    return {"success": True, "result": result}


@app.post("/api/check_inventory")
async def check_inventory_endpoint(request: CheckInventoryRequest):
    """Check inventory for paper stock."""
    if not MODULES.get('check_inventory'):
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": "check_inventory not available"}
        )
    
    result = MODULES['check_inventory'](
        request.paper_stock,
        request.color,
        request.finish
    )
    
    return {"success": True, "result": result}


@app.post("/api/check_resolution")
async def check_resolution_endpoint(request: CheckResolutionRequest):
    """Check file resolution."""
    if not MODULES.get('check_resolution'):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "check_resolution not available",
                "details": MODULES.get('resolution_error', 'Unknown error')
            }
        )
    
    result = MODULES['check_resolution'](request.file_path)
    return {"success": True, "result": result}


@app.post("/api/calculate_price")
async def calculate_price_endpoint(request: CalculatePriceRequest):
    """Calculate price for an order."""
    if not MODULES.get('calculate_price'):
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": "calculate_price not available"}
        )
    
    result = MODULES['calculate_price'](
        paper_stock=request.paper_stock,
        quantity=request.quantity,
        width_inches=request.width_inches,
        height_inches=request.height_inches,
        full_color=request.full_color,
        rush_type=request.rush_type
    )
    
    return {"success": True, "result": result}


@app.post("/api/test_guardrails")
async def test_guardrails():
    """Test the guardrail system."""
    if not MODULES.get('SpecCheckGuardrail'):
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": "Guardrails not available"}
        )
    
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
