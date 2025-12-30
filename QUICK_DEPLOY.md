# Quick Deploy Guide - Print Shop AI Order Guardrail PoC

## Quick Start (5 minutes)

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Test the System**
```bash
python3 main.py test-tools
python3 main.py test-guardrails
```

3. **Run Benchmark Tests**
```bash
python3 main.py benchmark
```

## System Architecture

✅ **Layer 1: Spec-Check Guardrail** - Validates order specifications
✅ **Layer 2: Pre-flight Guardrail** - Checks file resolution (300 DPI minimum)
✅ **Layer 3: Quote Guardrail** - Prevents price hallucinations

✅ **Three Tools**: `check_inventory`, `check_resolution`, `calculate_price`
✅ **ReAct Agent Loop**: Ready for LLM integration

## Next Step: LLM Integration

The core system is complete. To finish the PoC, integrate with an LLM provider:

1. Choose provider (OpenAI, Anthropic, etc.)
2. Update `agent/react_agent.py` to use LLM for reasoning
3. Feed benchmark orders through the system
4. Measure success rate

See `POC_IMPLEMENTATION.md` for full details.





