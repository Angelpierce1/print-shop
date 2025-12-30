# Print Shop AI Order Guardrail - PoC

**Hypothesis**: By implementing an AI Order Guardrail, we will reduce 'Pre-press Rejections' by 60% by catching file setup and spec errors before they reach a human technician.

## 🎯 Overview

This PoC implements a **multi-layered guardrail architecture** with three checkpoints:

1. **Layer 1: Spec-Check Guardrail (Input)** - Validates order specifications against shop capabilities
2. **Layer 2: Pre-flight Guardrail (Action)** - Verifies technical file specifications (PDFs/Images)
3. **Layer 3: Final Quote Guardrail (Output)** - Prevents price hallucinations

## 🏗️ Architecture

### Three-Layered Guardrail System

#### Layer 1: Spec-Check Guardrail
- **Location**: `guardrails/spec_check_guardrail.py`
- **Purpose**: Ensures customer orders are possible given shop capabilities
- **Implementation**: System prompt with Shop Capability Manifest
- **Example**: Rejects "Full-color printing on black 100lb cardstock" if white ink is not available

#### Layer 2: Pre-flight Guardrail  
- **Location**: `guardrails/preflight_guardrail.py`, `tools/resolution_tool.py`
- **Purpose**: Verifies technical file specifications
- **Implementation**: Python tool using Pillow (images) and PyMuPDF (PDFs)
- **Example**: Rejects files with resolution below 300 DPI

#### Layer 3: Final Quote Guardrail
- **Location**: `guardrails/quote_guardrail.py`
- **Purpose**: Prevents price hallucinations
- **Implementation**: Output validation that flags any "$" sign not from `calculate_price` tool
- **Example**: Flags response containing "$125.50" if `calculate_price` tool was not called

### Tools

The agent has access to three tools:

1. **`check_inventory(paper_stock, color, finish)`** - Validates paper stock availability
2. **`check_resolution(file_path)`** - Checks DPI/resolution of files (300 DPI minimum)
3. **`calculate_price(...)`** - Calculates pricing (MUST be used for all price quotes)

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Testing

```bash
# Test all tools
python3 main.py test-tools

# Test all guardrails
python3 main.py test-guardrails

# Run benchmark tests
python3 main.py benchmark
```

## 📁 Project Structure

```
print-shop/
├── agent/
│   └── react_agent.py          # ReAct loop implementation
├── config/
│   ├── shop_capabilities.json   # Shop capability manifest
│   └── pricing.json             # Pricing configuration
├── data/
│   ├── benchmark_orders.py      # Data structures for failed orders
│   └── benchmark_orders.json    # Sample benchmark orders
├── guardrails/
│   ├── spec_check_guardrail.py  # Layer 1: Input validation
│   ├── preflight_guardrail.py   # Layer 2: File validation
│   └── quote_guardrail.py       # Layer 3: Output validation
├── tools/
│   ├── inventory_tool.py        # Inventory checking tool
│   ├── resolution_tool.py       # Resolution checking tool
│   └── pricing_tool.py          # Pricing calculation tool
└── main.py                      # Main entry point
```

## 📊 PoC Execution Plan (6 Weeks)

### ✅ Week 1-2: The Data
- Collect 20 "Failed Orders" from the past year
- Create data structure for benchmark orders
- Sample benchmark orders included

### ✅ Week 3: The Agent
- Build ReAct loop structure
- Implement three tools
- Create multi-layered guardrail system

### 🔄 Week 4: The Loop
- Feed 20 failed orders into the agent
- Measure success rate (requires LLM integration)

### 📅 Week 5-6: Integration & Testing
- Integration with production system
- Real-world testing
- Performance measurement

## 🔧 Next Steps: LLM Integration

The core system is complete. To finish the PoC:

1. **Choose an LLM provider** (OpenAI, Anthropic, etc.)
2. **Implement the reasoning loop** in `agent/react_agent.py`:
   - Use LLM to parse user queries
   - Use LLM to decide which tool to call
   - Use LLM to formulate responses
3. **Apply system prompt** from `SpecCheckGuardrail.get_system_prompt()`
4. **Validate responses** using `QuoteGuardrail.validate_response()`

See `POC_IMPLEMENTATION.md` for detailed documentation.

## 📝 Configuration

### Shop Capabilities (`config/shop_capabilities.json`)
- Paper stocks and their available colors/finishes
- Printing capabilities (full color, white ink, etc.)
- File requirements (min DPI, formats, etc.)
- Size limits

### Pricing (`config/pricing.json`)
- Base prices per paper stock
- Quantity breaks and discounts
- Rush surcharges

## ✅ Success Criteria

The PoC succeeds if:
- ✅ Agent identifies errors in benchmark orders
- ✅ Agent asks users for corrections (new files, different specs)
- ✅ No price hallucinations (all prices from `calculate_price` tool)
- 🎯 60% reduction in pre-press rejections (measured in production)

## 📚 Documentation

- `POC_IMPLEMENTATION.md` - Detailed implementation guide
- `QUICK_DEPLOY.md` - Quick start guide
