# main.py
"""
Core Execution Orchestrator
Initializes decoupled asynchronous pipelines and handles risk handshake mechanics.
"""

import asyncio
import sys
from data_ingress import AsynchronousIngress
from alpha_gen import AlphaGenerator
from risk_manager import RiskManager

async def core_execution_loop():
    # Instantiate engine components once outside the ticker loop
    ingress = AsynchronousIngress()
    alpha = AlphaGenerator()       
    risk = RiskManager()
    
    print("\n" + "="*60)
    print("INITIALIZING QUANT WARFARE SYSTEM PHASE 2: ASYNC FRAMEWORK RUNTIME")
    print("="*60 + "\n")

    try:
        # Stream live tick data feed
        async for tick in ingress.stream_ticks():
            # Process tick via state-aware alpha layer
            signal = alpha.process_tick(tick)
            
            if signal:
                # 1. Ask Risk Manager for capital allocation authorization
                allocated_amount = risk.calculate_allocation(signal)
                
                # 2. Handshake: If capital allocation is approved (> 0), execute and log risk
                if allocated_amount > 0:
                    exec_price = risk.update_allocated_risk(
                        asset=signal["asset"],
                        direction=signal["direction"],
                        raw_price=signal["price"],
                        amount=allocated_amount
                    )
                    
                    print(f"[EXECUTION SUITE] ASSET: {signal['asset']} | DIR: {signal['direction']} | "
                          f"Stream Price: ${signal['price']:.2f} -> Filled Price: ${exec_price:.2f} | "
                          f"ALLOCATION: ${allocated_amount:,.2f} LOCKED")
                          
                elif signal["direction"] == "EXIT":
                    # Exit handshakes are explicitly logged internally by calculate_allocation()
                    pass
                    
    except KeyboardInterrupt:
        print("\n[SYSTEM TERMINATION] Execution cycle cleanly interrupted by operator. Exiting pipeline.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[CRITICAL RUNTIME ERROR] Exception detected in pipeline: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(core_execution_loop())