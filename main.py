# main.py
"""
Central Asynchronous Strategy Framework Orchestrator
Binds modules together inside a high-performance, non-blocking event runtime loop.
"""

import asyncio
from data_ingress import AsynchronousIngress
from alpha_gen import AlphaGenerator
from risk_manager import RiskManager

async def core_execution_loop():
    # Instantiate component-decoupled tracking modules
    ingress = AsynchronousIngress()
    alpha = AlphaGenerator()
    risk = RiskManager()
    
    print("=" * 70)
    print("INITIALIZING QUANT WARFARE SYSTEM PHASE 2: ASYNC FRAMEWORK RUNTIME")
    print("=" * 70)
    
    # Consume the streaming payload generator asynchronously using 'async for'
    async for tick_vector in ingress.stream_ticks():
        # Phase A: Pass raw price vectors to the alpha engine
        signal = alpha.process_tick(tick_vector)
        
        if signal:
                # Phase B: Pass verified alpha signals to the risk engine
                allocation_size = risk.calculate_allocation(signal)
                
                if allocation_size > 0:
                    # Update system state mapping with the full execution metrics
                    risk.update_allocated_risk(signal['asset'], signal['direction'], signal['price'], allocation_size)
                    
                    print(f"[EXECUTION SUITE] TIME: {tick_vector['timestamp']:.2f} | "
                        f"ASSET: {signal['asset']} | DIR: {signal['direction']} | "
                        f"PRICE: ${signal['price']} | ALLOCATION: ${allocation_size:,.2f} LOCKED")
                elif signal['direction'] != "EXIT":
                    print(f"[RISK REJECTION] Signal generated for {signal['asset']} but blocked by exposure caps.")
if __name__ == "__main__":
    # Initialize the high-performance async engine loop context
    try:
        asyncio.run(core_execution_loop())
    except KeyboardInterrupt:
        print("\n[SYSTEM TERMINATION] Execution cycle cleanly interrupted by operator. Exiting framework pipeline.")