# Asynchronous Systematic Strategy Framework (Project #031)

A production-grade, event-driven quantitative trading framework built from scratch in Python 3.11. This framework implements a multi-file, component-decoupled architecture to process concurrent multi-asset streams with dynamic, real-time capital allocation and defensive risk boundaries.

## System Architecture
The monorepo architecture enforces strict separation of concerns across 5 core decoupled modules:
- `config.py`: Global constants, multi-asset universes, and absolute portfolio risk thresholds.
- `data_ingress.py`: An asynchronous, non-blocking tick-generation simulation engine running on `asyncio`.
- `alpha_gen.py`: A momentum signal processing module tracking rolling caches to issue entry and exit triggers.
- `risk_manager.py`: A live state-machine accounting engine that sizes positions using the Kelly Criterion and recycles capital pools dynamically upon position liquidation.
- `main.py`: The high-performance event loop orchestrator.

## Core Mathematical Logic
Position sizing is dynamically calculated using a modified Half-Kelly Criterion model to optimize long-term log-wealth accumulation:

$$f^* = 0.50 \times \frac{b \cdot p - q}{b}$$

Where:
- $p$ = Win probability (0.54)
- $q$ = Loss probability (0.46)
- $b$ = Win-to-loss ratio (1.2)

The system enforces a hard `MAX_PORTFOLIO_EXPOSURE` at 80% of total capital to protect the fund from over-leveraging anomalies.