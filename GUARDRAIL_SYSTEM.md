# AI Order Guardrail System - Documentation

## Overview

This system implements a **three-layer AI Order Guardrail** to reduce pre-press rejections by 60% by catching file setup and spec errors before they reach human technicians.

## Architecture

### Layer 1: Spec-Check Guardrail (Input)
**Purpose:** Ensures the customer isn't ordering something impossible.

**Implementation:**
- Validates orders against `shop_capabilities.py` (Shop Capability Manifest)
- Checks paper types, ink capabilities, size limits, special services
- Rejects orders that don't match shop capabilities

**Example Failures:**
- "Full-color printing on black 100lb cardstock" → Rejected (no white ink)
- Size 20x30" → Rejected (max size is 13x19")
- Metallic ink request → Rejected (not available)

### Layer 2: Pre-flight Guardrail (Action)
**Purpose:** Verifies the technical files (PDFs/Images).

**Implementation:**
- Uses `check_resolution()` tool with Pillow/PyMuPDF
- Validates DPI (minimum 225, recommended 300)
- Checks pixel dimensions against target print size

**Example Failures:**
- 150 DPI image for 8x10" print → Rejected (below 225 minimum)
- Corrupted PDF → Rejected (file error)

### Layer 3: Final Quote Guardrail (Output)
**Purpose:** Prevents "Price Hallucinations."

**Implementation:**
- Agent MUST use `calculate_price()` tool
- Output guardrail flags any "$" sign not from official tool
- Ensures all prices come from pricing database, not AI estimation

**Example Failures:**
- Agent says "Price is $5.00" without calling tool → Rejected (hallucination)
- Agent estimates price → Rejected (must use tool)

## Tools Available to Agent

1. **`check_inventory(paper_type, quantity)`**
   - Checks if paper stock is available
   - Returns availability status and stock levels

2. **`check_resolution(file_path, width_inch, height_inch)`**
   - Validates image DPI quality
   - Returns quality assessment (high/acceptable/low)

3. **`calculate_price(size, paper_type, quantity)`**
   - **ONLY** source of truth for pricing
   - Returns detailed price breakdown

## Usage

### Basic Order Processing

```python
from agent import PrintShopAgent

agent = PrintShopAgent()

order_data = {
    'email': 'customer@example.com',
    'name': 'John Doe',
    'size': '8,10',  # or '8x10'
    'paper': '100lb Matte',
    'quantity': 50,
    'file_path': 'static/uploads/design.jpg',
    'filename': 'design.jpg'
}

result = agent.process_order(order_data)

if result['valid']:
    print(f"Order accepted! Price: {result['order_summary']['price']}")
else:
    print(f"Order rejected: {result['error']}")
```

### API Endpoints

**POST `/submit-order`**
- Submits order with full guardrail validation
- Returns success/error with detailed reasoning

**POST `/validate-order`**
- Validates order without submitting
- Useful for real-time feedback

## Testing with Failed Orders

To test the system with historical failed orders:

1. Create a `benchmark_orders/` directory
2. Add 20 failed orders as JSON files
3. Run validation script:

```python
python test_benchmark.py
```

## Success Metrics

- **Target:** 60% reduction in pre-press rejections
- **Measurement:** Compare rejection rate before/after implementation
- **Benchmark:** Test against 20 historical failed orders

## File Structure

```
print-shop/
├── app.py                    # Flask app with agent integration
├── agent.py                  # ReAct agent with guardrails
├── tools.py                  # Three agent tools
├── shop_capabilities.py      # Shop capability manifest
├── requirements.txt          # Dependencies
└── GUARDRAIL_SYSTEM.md       # This file
```

## Next Steps (PoC Execution)

1. **Week 1-2:** Collect 20 "Failed Orders" from past year
2. **Week 3:** Test agent against benchmark set
3. **Week 4:** Measure success rate (target: 60% error detection)
4. **Week 5-6:** Refine and deploy

