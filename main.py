"""Main entry point for the Print Shop AI Order Guardrail PoC."""

import sys
from pathlib import Path
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from agent.react_agent import ReActAgent
from data.benchmark_orders import load_benchmark_orders, BenchmarkOrder
from guardrails.spec_check_guardrail import SpecCheckGuardrail
from guardrails.preflight_guardrail import PreflightGuardrail
from guardrails.quote_guardrail import QuoteGuardrail


def test_guardrails():
    """Test the three guardrail layers."""
    print("=" * 60)
    print("Testing Multi-Layered Guardrail System")
    print("=" * 60)
    
    # Layer 1: Spec-Check Guardrail
    print("\n[Layer 1] Spec-Check Guardrail")
    print("-" * 60)
    spec_guardrail = SpecCheckGuardrail()
    
    # Test: Impossible order (full color on black paper)
    test_order = {
        "paper_stock": "100lb_cardstock",
        "color": "black",
        "finish": "matte",
        "full_color": True,
        "dark_paper": True
    }
    
    result = spec_guardrail.validate_order_spec(test_order)
    print(f"Test Order: Full color on black 100lb cardstock")
    print(f"Valid: {result['valid']}")
    if result['errors']:
        print(f"Errors: {', '.join(result['errors'])}")
    
    # Layer 2: Pre-flight Guardrail
    print("\n[Layer 2] Pre-flight Guardrail")
    print("-" * 60)
    preflight_guardrail = PreflightGuardrail()
    
    # Note: This would need an actual file to test
    print("Pre-flight guardrail ready (requires file to test)")
    
    # Layer 3: Quote Guardrail
    print("\n[Layer 3] Final Quote Guardrail")
    print("-" * 60)
    quote_guardrail = QuoteGuardrail()
    
    # Test: Price without tool
    test_response = "The price for your order will be $125.50"
    test_tool_calls = []  # No tool calls
    
    result = quote_guardrail.validate_response(test_response, test_tool_calls)
    print(f"Test Response: '{test_response}'")
    print(f"Valid: {result['valid']}")
    if not result['valid']:
        print(f"Error: {result['error']}")
        print(f"Violation: {result.get('violation')}")
    
    # Test: Price with tool
    test_tool_calls_with_price = [{"tool_name": "calculate_price"}]
    result2 = quote_guardrail.validate_response(test_response, test_tool_calls_with_price)
    print(f"\nTest Response with pricing tool: '{test_response}'")
    print(f"Valid: {result2['valid']}")


def test_tools():
    """Test the three tools."""
    print("\n" + "=" * 60)
    print("Testing Tools")
    print("=" * 60)
    
    from tools.inventory_tool import check_inventory
    from tools.pricing_tool import calculate_price
    
    # Test check_inventory
    print("\n[Tool] check_inventory")
    print("-" * 60)
    result = check_inventory("100lb_cardstock", "white", "matte")
    print(f"Input: 100lb_cardstock, white, matte")
    print(f"Result: {result}")
    
    result2 = check_inventory("100lb_cardstock", "black", "matte")
    print(f"\nInput: 100lb_cardstock, black, matte")
    print(f"Result: {result2}")
    
    # Test calculate_price
    print("\n[Tool] calculate_price")
    print("-" * 60)
    price_result = calculate_price(
        paper_stock="100lb_cardstock",
        quantity=500,
        width_inches=3.5,
        height_inches=2.0,
        full_color=True
    )
    print(f"Input: 100lb_cardstock, 500 qty, 3.5x2.0, full color")
    print(f"Result: ${price_result.get('total_price', 0):.2f}")


def run_benchmark_test():
    """Run benchmark orders through the agent."""
    print("\n" + "=" * 60)
    print("Running Benchmark Tests")
    print("=" * 60)
    
    orders = load_benchmark_orders()
    
    if not orders:
        print("No benchmark orders found. Create benchmark_orders.json first.")
        return
    
    agent = ReActAgent()
    
    caught_count = 0
    total_count = len(orders)
    
    for order in orders:
        print(f"\n[Order {order.order_id}]")
        print("-" * 60)
        print(f"Request: {order.customer_request}")
        print(f"Rejection Reason: {order.rejection_reason}")
        print(f"Category: {order.rejection_category}")
        print(f"Expected to catch: {order.should_catch_error}")
        
        # Process order through agent
        # In full implementation, this would use LLM
        result = agent.process_order(
            user_query=order.customer_request,
            file_path=order.file_path
        )
        
        if result.get("status") == "rejected":
            caught_count += 1
            print(f"✓ Agent caught the error")
        else:
            print(f"✗ Agent did not catch the error")
    
    print("\n" + "=" * 60)
    print(f"Results: {caught_count}/{total_count} errors caught ({caught_count/total_count*100:.1f}%)")
    print("=" * 60)


def main():
    """Main function."""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "test-guardrails":
            test_guardrails()
        elif command == "test-tools":
            test_tools()
        elif command == "benchmark":
            run_benchmark_test()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: test-guardrails, test-tools, benchmark")
    else:
        print("Print Shop AI Order Guardrail PoC")
        print("\nAvailable commands:")
        print("  python main.py test-guardrails  - Test all guardrail layers")
        print("  python main.py test-tools       - Test all tools")
        print("  python main.py benchmark        - Run benchmark order tests")
        print("\nOr run test_guardrails() for a quick demo")


if __name__ == "__main__":
    main()

