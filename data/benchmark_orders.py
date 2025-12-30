"""Data structure for storing benchmark orders (failed orders from past year)."""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import json
from pathlib import Path

@dataclass
class BenchmarkOrder:
    """Represents a failed order from historical data."""
    order_id: str
    customer_request: str
    file_path: Optional[str]
    paper_stock: Optional[str]
    color: Optional[str]
    finish: Optional[str]
    quantity: Optional[int]
    width_inches: Optional[float]
    height_inches: Optional[float]
    full_color: Optional[bool]
    
    # Failure details
    rejection_reason: str
    rejection_category: str  # "wrong_size", "low_res", "missing_bleed", "impossible_spec", etc.
    rejection_date: str
    
    # Expected agent behavior
    expected_agent_action: str  # What the agent should do
    should_catch_error: bool  # Whether agent should catch this error

def load_benchmark_orders(file_path: Optional[Path] = None) -> List[BenchmarkOrder]:
    """Load benchmark orders from JSON file."""
    if file_path is None:
        file_path = Path(__file__).parent / "benchmark_orders.json"
    
    if not file_path.exists():
        return []
    
    with open(file_path, "r") as f:
        data = json.load(f)
    
    return [BenchmarkOrder(**order) for order in data]

def save_benchmark_orders(orders: List[BenchmarkOrder], file_path: Optional[Path] = None):
    """Save benchmark orders to JSON file."""
    if file_path is None:
        file_path = Path(__file__).parent / "benchmark_orders.json"
    
    data = [asdict(order) for order in orders]
    
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

def create_sample_benchmark_orders() -> List[BenchmarkOrder]:
    """Create sample benchmark orders for PoC testing."""
    return [
        BenchmarkOrder(
            order_id="FAIL-001",
            customer_request="I need 500 business cards on black 100lb cardstock, full color",
            file_path=None,
            paper_stock="100lb_cardstock",
            color="black",
            finish="matte",
            quantity=500,
            width_inches=3.5,
            height_inches=2.0,
            full_color=True,
            rejection_reason="Full color on black paper requires white ink, which we don't have",
            rejection_category="impossible_spec",
            rejection_date="2024-01-15",
            expected_agent_action="Reject order, explain white ink limitation, suggest white paper",
            should_catch_error=True
        ),
        BenchmarkOrder(
            order_id="FAIL-002",
            customer_request="Print 1000 flyers, file attached",
            file_path="sample_low_res.jpg",
            paper_stock="80lb_text",
            color="white",
            finish="gloss",
            quantity=1000,
            width_inches=8.5,
            height_inches=11.0,
            full_color=True,
            rejection_reason="File resolution is only 72 DPI, need minimum 300 DPI",
            rejection_category="low_res",
            rejection_date="2024-02-20",
            expected_agent_action="Reject file, request higher resolution file",
            should_catch_error=True
        ),
        BenchmarkOrder(
            order_id="FAIL-003",
            customer_request="Print 50 posters, 24x36 inches",
            file_path=None,
            paper_stock="100lb_cardstock",
            color="white",
            finish="matte",
            quantity=50,
            width_inches=24.0,
            height_inches=36.0,
            full_color=True,
            rejection_reason="Size 24x36 exceeds maximum 12x18 inches",
            rejection_category="wrong_size",
            rejection_date="2024-03-10",
            expected_agent_action="Reject order, explain size limitations",
            should_catch_error=True
        ),
        # Add more sample orders as needed
    ]





