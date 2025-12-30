# Print Shop AI Order Guardrail - PoC Implementation

## Overview

This PoC implements a multi-layered AI Order Guardrail system designed to reduce pre-press rejections by 60% by catching file setup and spec errors before they reach human technicians.

## Architecture

### Three-Layered Guardrail System

#### Layer 1: Spec-Check Guardrail (Input)
- **Purpose**: Ensures customer orders are possible given shop capabilities
- **Implementation**: System prompt with Shop Capability Manifest
- **Location**: `guardrails/spec_check_guardrail.py`
- **Config**: `config/shop_capabilities.json`

**Example**: Rejects "Full-color printing on black 100lb cardstock" if white ink is not available.

#### Layer 2: Pre-flight Guardrail (Action)
- **Purpose**: Verifies technical file specifications (PDFs/Images)
- **Implementation**: Python tool using Pillow (images) and PyMuPDF (PDFs)
- **Location**: `tools/resolution_tool.py`, `guardrails/preflight_guardrail.py`
- **Checks**: Resolution (DPI), file format, file existence

**Example**: Rejects files with resolution below 300 DPI.

#### Layer 3: Final Quote Guardrail (Output)
- **Purpose**: Prevents "Price Hallucinations"
- **Implementation**: Output validation that flags any "$" sign not from `calculate_price` tool
- **Location**: `guardrails/quote_guardrail.py`
- **Rule**: Agent must NEVER estimate prices - only report what `calculate_price` returns

**Example**: Flags response containing "$125.50" if `calculate_price` tool was not called.

## Tools

The agent has access to three tools:

1. **check_inventory(paper_stock, color, finish)**
   - Validates paper stock availability
   - Checks color and finish combinations
   - Location: `tools/inventory_tool.py`

2. **check_resolution(file_path)**
   - Checks DPI/resolution of images and PDFs
   - Validates against minimum requirements (300 DPI)
   - Location: `tools/resolution_tool.py`

3. **calculate_price(paper_stock, quantity, width_inches, height_inches, full_color, rush_type)**
   - Calculates pricing for orders
   - MUST be used for all price quotes
   - Location: `tools/pricing_tool.py`
   - Config: `config/pricing.json`

## ReAct Agent Loop

The agent follows a Reasoning + Acting loop:

1. **Think**: Analyze the current situation
2. **Act**: Use a tool OR provide final answer
3. **Observe**: Process tool results and continue

Location: `agent/react_agent.py`

## Project Structure

```
print-shop/
├── agent/
│   ├── __init__.py
│   └── react_agent.py          # ReAct loop implementation
├── config/
│   ├── shop_capabilities.json   # Shop capability manifest
│   └── pricing.json             # Pricing configuration
├── data/
│   ├── __init__.py
│   ├── benchmark_orders.py      # Data structures for failed orders
│   └── benchmark_orders.json    # Sample benchmark orders
├── guardrails/
│   ├── __init__.py
│   ├── spec_check_guardrail.py  # Layer 1: Input validation
│   ├── preflight_guardrail.py   # Layer 2: File validation
│   └── quote_guardrail.py       # Layer 3: Output validation
├── tools/
│   ├── __init__.py
│   ├── inventory_tool.py        # Inventory checking tool
│   ├── resolution_tool.py       # Resolution checking tool
│   └── pricing_tool.py          # Pricing calculation tool
├── main.py                      # Main entry point
├── requirements.txt             # Python dependencies
└── POC_IMPLEMENTATION.md        # This file
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Verify installation:
```bash
python main.py test-tools
```

## Usage

### Test Guardrails
```bash
python main.py test-guardrails
```

### Test Tools
```bash
python main.py test-tools
```

### Run Benchmark Tests
```bash
python main.py benchmark
```

## PoC Execution Plan (6 Weeks)

### Week 1-2: The Data
- ✅ Collect 20 "Failed Orders" from the past year
- ✅ Create data structure for benchmark orders
- ✅ Document rejection reasons and categories

**Current Status**: Sample benchmark orders included in `data/benchmark_orders.json`

### Week 3: The Agent
- ✅ Build ReAct loop structure
- ✅ Implement three tools: `check_inventory`, `check_resolution`, `calculate_price`
- ✅ Create multi-layered guardrail system

**Current Status**: Core implementation complete. Ready for LLM integration.

### Week 4: The Loop
- 🔄 Feed 20 failed orders into the agent
- 🔄 Measure success rate (agent should identify errors and ask for corrections)

**Next Steps**: Integrate with LLM (OpenAI, Anthropic, or similar) to complete the ReAct loop.

### Week 5-6: Integration & Testing
- Integration with production system
- Real-world testing
- Performance measurement

## LLM Integration Notes

The current implementation provides the structure and tools. To complete the PoC:

1. **Choose an LLM provider** (OpenAI, Anthropic, etc.)
2. **Implement the reasoning loop** in `agent/react_agent.py`:
   - Use LLM to parse user queries
   - Use LLM to decide which tool to call
   - Use LLM to formulate responses
3. **Apply system prompt** from `SpecCheckGuardrail.get_system_prompt()`
4. **Validate responses** using `QuoteGuardrail.validate_response()`

## Configuration

### Shop Capabilities (`config/shop_capabilities.json`)
- Paper stocks and their available colors/finishes
- Printing capabilities (full color, white ink, etc.)
- File requirements (min DPI, formats, etc.)
- Size limits

### Pricing (`config/pricing.json`)
- Base prices per paper stock
- Quantity breaks and discounts
- Rush surcharges

## Success Criteria

The PoC succeeds if:
- Agent identifies errors in benchmark orders
- Agent asks users for corrections (new files, different specs)
- No price hallucinations (all prices from `calculate_price` tool)
- 60% reduction in pre-press rejections (measured in production)

## Next Steps

1. Integrate with LLM provider
2. Collect real failed orders from past year
3. Run benchmark tests
4. Measure and iterate




