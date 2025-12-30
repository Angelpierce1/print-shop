"""
Test script for AI Order Guardrail System
Tests the agent against various order scenarios.
"""

import os
from agent import PrintShopAgent
from PIL import Image
import tempfile

# Create test agent
agent = PrintShopAgent()

def create_test_image(width_px, height_px, filename):
    """Create a test image with specific dimensions"""
    img = Image.new('RGB', (width_px, height_px), color='white')
    filepath = os.path.join('static/uploads', filename)
    os.makedirs('static/uploads', exist_ok=True)
    img.save(filepath, 'JPEG')
    return filepath

def test_order_scenario(name, order_data, expected_result):
    """Test a single order scenario"""
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print(f"{'='*60}")
    
    result = agent.process_order(order_data)
    
    if result['valid'] == expected_result:
        status = "✅ PASS"
    else:
        status = "❌ FAIL"
    
    print(f"Status: {status}")
    print(f"Expected: {'Valid' if expected_result else 'Invalid'}")
    print(f"Got: {'Valid' if result['valid'] else 'Invalid'}")
    
    if not result['valid']:
        print(f"Error: {result.get('error', result.get('message', 'Unknown error'))}")
        print(f"Layer: {result.get('layer', 'unknown')}")
    
    if result['valid']:
        print(f"Price: {result['order_summary']['price']}")
        print(f"Quality: {result['order_summary']['file_quality']['quality']}")
    
    print(f"\nReasoning Steps:")
    for step in result.get('reasoning', []):
        print(f"  {step}")
    
    return result['valid'] == expected_result

# Test Scenarios
def run_tests():
    """Run all test scenarios"""
    print("="*60)
    print("AI ORDER GUARDRAIL SYSTEM - TEST SUITE")
    print("="*60)
    
    results = []
    
    # Test 1: Valid order (should pass)
    test_file = create_test_image(2400, 3000, 'test_high_quality.jpg')  # 300 DPI for 8x10
    results.append(test_order_scenario(
        "Valid Order - High Quality",
        {
            'email': 'test@example.com',
            'size': '8,10',
            'paper': '100lb Matte',
            'quantity': 10,
            'file_path': test_file,
            'filename': 'test_high_quality.jpg'
        },
        expected_result=True
    ))
    
    # Test 2: Low DPI (should fail Layer 2)
    test_file = create_test_image(800, 1000, 'test_low_dpi.jpg')  # ~100 DPI for 8x10
    results.append(test_order_scenario(
        "Low DPI - Should Fail",
        {
            'email': 'test@example.com',
            'size': '8,10',
            'paper': '100lb Matte',
            'quantity': 10,
            'file_path': test_file,
            'filename': 'test_low_dpi.jpg'
        },
        expected_result=False
    ))
    
    # Test 3: Invalid paper (should fail Layer 1)
    test_file = create_test_image(2400, 3000, 'test_invalid_paper.jpg')
    results.append(test_order_scenario(
        "Invalid Paper Type - Should Fail",
        {
            'email': 'test@example.com',
            'size': '8,10',
            'paper': 'Black cardstock with white ink',
            'quantity': 10,
            'file_path': test_file,
            'filename': 'test_invalid_paper.jpg'
        },
        expected_result=False
    ))
    
    # Test 4: Size too large (should fail Layer 1)
    test_file = create_test_image(2400, 3000, 'test_oversized.jpg')
    results.append(test_order_scenario(
        "Oversized Print - Should Fail",
        {
            'email': 'test@example.com',
            'size': '20,30',
            'paper': '100lb Matte',
            'quantity': 10,
            'file_path': test_file,
            'filename': 'test_oversized.jpg'
        },
        expected_result=False
    ))
    
    # Test 5: Acceptable DPI (should pass)
    test_file = create_test_image(1800, 2250, 'test_acceptable.jpg')  # 225 DPI for 8x10
    results.append(test_order_scenario(
        "Acceptable DPI - Should Pass",
        {
            'email': 'test@example.com',
            'size': '8,10',
            'paper': '100lb Matte',
            'quantity': 10,
            'file_path': test_file,
            'filename': 'test_acceptable.jpg'
        },
        expected_result=True
    ))
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    print(f"Success Rate: {passed/total*100:.1f}%")
    
    return passed == total

if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)

