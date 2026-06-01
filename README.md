# Asynchronous Systematic Strategy Framework (Phase 2 Portfolio)

A production-grade, event-driven quantitative trading framework built to simulate multi-asset execution loops, dynamic risk budgeting, and real-world market friction.

## 📈 Project #031: Core Asynchronous Architecture
The initial footprint established a decoupled, non-blocking state machine using `asyncio` to ingest streaming price vectors and manage capital allocations.

- **Allocation Math:** Implemented a Half-Kelly Criterion model to safely size positions based on a unified liquid capital pool (\$100,000 baseline).
- **Risk Boundaries:** Enforced a hard portfolio exposure cap at 80% to protect the system against margin anomalies.

---

## 🚨 Project #032: Friction Simulation & Alpha Filtering (Current)
Recognizing that "perfect execution" backtests are an illusion, this upgrade introduced real-world broker and order book dynamics to expose and correct alpha leakage.

### 1. Execution Friction Models
- **Stochastic Slippage:** Implemented a random-variance slippage model (up to 15 basis points) that degrades execution prices (fills entries higher on longs and liquidates exits lower).
- **Fixed Commissions:** Injected a flat \$2.00 broker ticket fee per execution.

### 2. Alpha Defense Framework
Initial runs revealed that high-frequency trading of micro-movements caused transaction fees to aggressively drain the capital pool. 

To defeat this, a **Velocity Threshold Filter** was engineered inside `alpha_gen.py`. The engine now measures absolute price delta over a 5-tick rolling window and explicitly blocks signals unless the structural price velocity can safely absorb expected transaction costs:

| Asset | Minimum Price Delta Entry Threshold |
| :--- | :--- |
| **BTC/USD** | \$12.00 |
| **ETH/USD** | \$1.50 |
| **SOL/USD** | \$0.15 |

*Outcome: Reduced over-trading frequency, minimized slippage metrics, and preserved capital pool longevity during market chop.*